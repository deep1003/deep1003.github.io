"""Publication text plates linked to cached token-position concept alignments."""
from pathlib import Path
import json,re,hashlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextToPath
from matplotlib.patches import Rectangle,ConnectionPatch
from plot_style import (CONDITION_ORDER,CONDITION_COLORS,CONCEPT_ORDER,activation_cmap,heatmap_text_color)
from english_figures import style,save

BASE=Path(__file__).resolve().parent
DATA=BASE
NAMES=['UN','FA','Calm','Sadness','Anger','Desperation','Joy']
FONT=FontProperties(family='AppleGothic')
MEASURE=TextToPath()
LIMITS=(-.20,.10)


def segments(text):
    """Non-overlapping sentence spans, including the original whitespace."""
    starts=[0]+[m.end() for m in re.finditer(r'\n\n|(?<=\.)\s+(?=[가-힣])',text)]
    starts=sorted(set(starts+[len(text)]))
    return [(a,z) for a,z in zip(starts,starts[1:]) if text[a:z].strip()]


def wrap_span(text,a,z,width,size):
    prop=FONT.copy();prop.set_size(size)
    widths={c:MEASURE.get_text_width_height_descent(c,prop,False)[0] for c in set(text[a:z]) if c not in '\r\n'}
    lines=[];line=[];used=0.
    for word in re.finditer(r'[^\S\r\n]+|\S+|[\r\n]+',text[a:z]):
        token=word.group();start=a+word.start()
        if '\n' in token or '\r' in token:
            if line:lines.append(line);line=[];used=0.
            continue
        total=sum(widths[c] for c in token)
        if not token.isspace() and line and used+total>width:
            lines.append(line);line=[];used=0.
        if token.isspace() and not line:continue
        for j,c in enumerate(token):
            w=widths[c]
            if line and used+w>width:
                lines.append(line);line=[];used=0.
            line.append((start+j,c,used,w));used+=w
    if line:lines.append(line)
    return lines


def row(fig,p,bottom,height,axis,letter,size=7.1):
    norm=Normalize(*LIMITS);cmap=activation_cmap();ci=CONCEPT_ORDER.index(axis)
    original=p['text'];chars=p['layers']['16'];values=np.array([r['cosine'] for r in chars],float)
    assert ''.join(r['char'] for r in chars)==original and values.shape==(len(original),7)
    # Physical points make character placement independent of raster resolution.
    fw,fh=fig.get_size_inches()*72
    left=.095;heat_w=.19;right=.40;right_w=.56
    ax=fig.add_axes([left,bottom,heat_w,height])
    im=ax.imshow(values,aspect='auto',origin='upper',cmap=cmap,norm=norm,interpolation='none',rasterized=True)
    ax.set_xticks(range(7),['UN','FA','Calm','Sad.','Ang.','Desp.','Joy'],rotation=45,ha='right',fontsize=5.5)
    ax.set_yticks([0,len(original)-1],['1',str(len(original))],fontsize=6)
    ax.set_ylabel('Character position',fontsize=6.5,labelpad=3)
    ax.tick_params(length=0,pad=2)
    for spine in ax.spines.values():spine.set_visible(False)
    label={'UN0FA0':'00  Reference','UN0FA1':'01  FA only','UN1FA0':'10  UN only','UN1FA1':'11  UN + FA'}[p['condition']]
    fig.text(.04,bottom+height+.010,letter,weight='bold',fontsize=8)
    fig.text(left,bottom+height+.010,label,color=CONDITION_COLORS[p['condition']],fontsize=8,weight='bold')
    tx=fig.add_axes([right,bottom,right_w,height]);width=right_w*fw;h=height*fh
    tx.set_xlim(0,width);tx.set_ylim(0,h);tx.axis('off')
    spans=segments(original)
    line_h=size+2.9;gap=5.5;padding=3.
    for _ in range(10):
        wrapped=[wrap_span(original,a,z,width-2*padding,size) for a,z in spans]
        used=sum(len(lines)*line_h+2*padding+gap for lines in wrapped)-gap
        if used<=h:break
        size-=.2;line_h-=.2;gap-=.2
    assert used<=h, 'Text plate overflow'
    top=h
    for k,((a,z),lines) in enumerate(zip(spans,wrapped)):
        box_h=len(lines)*line_h+2*padding
        tx.add_patch(Rectangle((0,top-box_h),width,box_h,facecolor='white',edgecolor='#777777',lw=.35))
        for r,line in enumerate(lines):
            y=top-padding-r*line_h
            for i,c,x,w in line:
                if c.isspace():continue
                value=values[i,ci]
                tx.add_patch(Rectangle((padding+x,y-line_h+.5),max(w,.5),line_h,
                                      facecolor=cmap(norm(value)),edgecolor='none'))
                tx.text(padding+x,y,c,fontproperties=FONT,fontsize=size,va='top',
                        color=heatmap_text_color(cmap,norm,value))
        # Link the exact span midpoint in the heatmap to the matching original text box.
        fig.add_artist(ConnectionPatch(xyA=(6.65,(a+z-1)/2),coordsA=ax.transData,
                       xyB=(0,top-box_h/2),coordsB=tx.transData,color='#777777',lw=.45,
                       clip_on=False,zorder=1))
        ax.plot([6.65,6.65],[a-.5,z-.5],color='#555555',lw=.6,clip_on=False)
        top-=box_h+gap
    return im


def build(axis='FA',show=False):
    assert axis in CONCEPT_ORDER
    style();payload=json.loads((DATA/'highlights.json').read_text())
    prompts=[next(p for p in payload['prompts'] if p['condition']==c) for c in CONDITION_ORDER]
    fig=plt.figure(figsize=(180/25.4,260/25.4))
    fig.text(.04,.979,'EXAONE prompt text and internal alignment',fontsize=10,weight='bold')
    fig.text(.095,.953,'Seven-axis overview',fontsize=7)
    fig.text(.40,.953,f'Original Korean prompt; background = {axis} alignment',fontsize=7)
    for i,p in enumerate(prompts):im=row(fig,p,.748-i*.218,.173,axis,'abcd'[i])
    cb=fig.colorbar(im,cax=fig.add_axes([.40,.064,.50,.011]),orientation='horizontal',ticks=[-.20,-.10,0,.10])
    cb.ax.tick_params(labelsize=6,length=2);cb.set_label('Centered cosine alignment, layer 16',fontsize=7)
    fig.text(.04,.009,'Backgrounds show measured hidden-state alignment, not token attribution or experienced emotion.',fontsize=6)
    path=save(fig,BASE/'figures',f'Prompt_text_activation_{axis}_en',show)
    for p in prompts:
        single=plt.figure(figsize=(180/25.4,100/25.4))
        single.text(.04,.95,'EXAONE prompt text and internal alignment',fontsize=10,weight='bold')
        image=row(single,p,.22,.64,axis,'',size=9.0)
        bar=single.colorbar(image,cax=single.add_axes([.40,.14,.50,.025]),orientation='horizontal',ticks=[-.20,-.10,0,.10])
        bar.ax.tick_params(labelsize=7,length=2);bar.set_label(f'Centered cosine alignment, layer 16; text axis = {axis}',fontsize=8)
        single.text(.04,.022,'Exact Korean stimulus; contextual alignment, not causal token contribution.',fontsize=7)
        save(single,BASE/'figures',f'Prompt_text_activation_{axis}_{p["condition"]}_en',False)
    records=[]
    for p in prompts:
        for i,r in enumerate(p['layers']['16']):
            records.append(dict(condition=p['condition'],character_index=i,character=r['char'],
                                source_tokens=r['tokens'],cosine=dict(zip(CONCEPT_ORDER,r['cosine']))))
    (BASE/'figures'/'Prompt_text_activation_source.json').write_text(json.dumps(records,ensure_ascii=False))
    provenance={'source_sha256':hashlib.sha256((DATA/'highlights.json').read_bytes()).hexdigest(),
                'axis':axis,'layer':16,'limits':list(LIMITS),'condition_order':CONDITION_ORDER,
                'normalization':'One fixed signed color range across all concepts and four prompts.',
                'character_mapping':'Original offsets; overlapping token fragments averaged by the unchanged collector.',
                'language':'English figure labels; exact measured Korean stimulus retained.',
                'model_inference':False,'interpretation':'Contextual hidden-state alignment, not causal token contribution.'}
    (BASE/'figures'/f'Prompt_text_activation_{axis}_provenance.json').write_text(json.dumps(provenance,indent=2))
    return path

if __name__=='__main__':
    build('FA')
