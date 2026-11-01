# Qwen 7B와14B 최소설계 짝비교

두모델각5184개,108문항48조건을검증했다. 모든216개위협/기록입력문자열해시가동일하다. 모델별8축을동일절차로별도추출했다.

원고·Overleaf·홈페이지는수정하지않았다. 본비교는선정된108문항에조건부인탐색적비교이며단두규모로일반적인규모추세를입증하지않는다. 14B는메모리를위해batch1,7B는최대6이다. 정밀도bf16·MPS·eager와상대깊이0.5는같다.

## 전체 위협 효과와 직접 차이

```csv
metric,seven_effect_pp,fourteen_effect_pp,difference14minus7_pp,ci_lo_pp,ci_hi_pp
p_unknown,7.676959059302281,2.2074907690116445,-5.469468290290637,-10.701896588041576,-0.584066287692505
full_unknown,7.650899304556952,11.437590010173132,3.786690705616185,-1.3281383992107076,8.91126193345486

```

## 각 모델의 제거·재현 비중

```csv
model,metric,direction,component,share_percent,ci_lo,ci_hi,denominator_established
7B,p_unknown,remove,full,9.583774206212324,3.0359252602273137,23.099238892219,True
14B,p_unknown,remove,full,,,,False
7B,p_unknown,remove,emo,2.76086053675165,0.0988514533606489,7.236057905162991,True
14B,p_unknown,remove,emo,,,,False
7B,p_unknown,remove,res,9.380936375153642,2.7559078447432515,23.690714767527226,True
14B,p_unknown,remove,res,,,,False
7B,p_unknown,add,full,6.94610528733047,-0.39673323644012787,21.508321687728962,True
14B,p_unknown,add,full,,,,False
7B,p_unknown,add,emo,-1.335180754738523,-3.9285772456512444,0.6402708217040128,True
14B,p_unknown,add,emo,,,,False
7B,p_unknown,add,res,7.935697683347299,0.8663505731885421,21.229516692194593,True
14B,p_unknown,add,res,,,,False
7B,full_unknown,remove,full,9.406087068779865,2.9212504437172333,22.900503274067674,True
14B,full_unknown,remove,full,22.613639146934066,14.997915018784333,33.54880286804545,True
7B,full_unknown,remove,emo,2.7479464600957852,0.08363090428252244,7.243997282939656,True
14B,full_unknown,remove,emo,-0.6186465454489767,-2.9254682655657662,1.2887991585112066,True
7B,full_unknown,remove,res,9.301062690738407,2.701984990655051,23.662462826311433,True
14B,full_unknown,remove,res,23.633770930735462,16.40178071005692,34.212649340172916,True
7B,full_unknown,add,full,6.957937753677397,-0.40702836410753873,21.584350636201037,True
14B,full_unknown,add,full,54.50698667840526,40.61985738342303,74.76395286360417,True
7B,full_unknown,add,emo,-1.350424344525649,-3.954953660365213,0.6186632463399725,True
14B,full_unknown,add,emo,1.0243009571352457,-2.2953407742603043,4.216882643218814,True
7B,full_unknown,add,res,7.959036558637976,0.8672982742752998,21.484177041966127,True
14B,full_unknown,add,res,53.46092542148624,40.0857443499938,72.86533147657516,True

```

## 문항별 효과의 직접 모델 차이

두모델효과의유의성유무를비교하지않고,동일문항의효과또는비중을직접뺐다. 비중차이는각모델의분모가성립할때만보고한다.

```csv
metric,direction,component,quantity,difference14minus7,ci_lo,ci_hi,interpretable
p_unknown,remove,full,raw_effect_pp,-0.5773533363154779,-1.193130205060955,-0.013663847188341106,True
p_unknown,remove,full,share_percentage_points,,,,False
p_unknown,remove,emo,raw_effect_pp,-0.2016347534948297,-0.4568797680028707,0.02682828629126159,True
p_unknown,remove,emo,share_percentage_points,,,,False
p_unknown,remove,res,raw_effect_pp,-0.6056590103776103,-1.2323799916966658,-0.034659612023928726,True
p_unknown,remove,res,share_percentage_points,,,,False
p_unknown,remove,emotion_minus_matched_random,raw_effect_pp,-0.2249683893534622,-0.48171409525464837,0.00943288057368758,True
p_unknown,add,full,raw_effect_pp,-0.21384315096953826,-1.1344915131679494,0.6142716805954526,True
p_unknown,add,full,share_percentage_points,,,,False
p_unknown,add,emo,raw_effect_pp,0.2691255349250269,0.05838978488197655,0.5201778441465771,True
p_unknown,add,emo,share_percentage_points,,,,False
p_unknown,add,res,raw_effect_pp,-0.4440696766590469,-1.2431423316797878,0.274632335560038,True
p_unknown,add,res,share_percentage_points,,,,False
p_unknown,add,emotion_minus_matched_random,raw_effect_pp,0.2223981769104705,-0.00874502169054637,0.494572413183944,True
full_unknown,remove,full,raw_effect_pp,1.866805081875031,0.8558530157203109,2.967547761786692,True
full_unknown,remove,full,share_percentage_points,13.207552078154201,-1.1788146955973207,25.888809084050386,True
full_unknown,remove,emo,raw_effect_pp,-0.2810008720856192,-0.6277572262927048,0.037328519538543756,True
full_unknown,remove,emo,share_percentage_points,-3.366593005544762,-8.361597778098243,0.06411755474502175,True
full_unknown,remove,res,raw_effect_pp,1.9915188822788896,0.992746282204237,3.077329527080085,True
full_unknown,remove,res,share_percentage_points,14.332708239997055,-0.6305570139070127,26.76110029647131,True
full_unknown,remove,emotion_minus_matched_random,raw_effect_pp,-0.3437521366357348,-0.6774710097628552,-0.04604101793531506,True
full_unknown,add,full,raw_effect_pp,5.701940851968071,4.025584167794794,7.5490019303821185,True
full_unknown,add,full,share_percentage_points,47.54904892472786,28.3730558348359,68.86969185061749,True
full_unknown,add,emo,raw_effect_pp,0.22047495073128928,-0.1881408803666783,0.6247546287736063,True
full_unknown,add,emo,share_percentage_points,2.3747253016608947,-1.7428810911601156,6.971818891569271,True
full_unknown,add,res,raw_effect_pp,5.505703592639752,3.952226058508222,7.308411567209233,True
full_unknown,add,res,share_percentage_points,45.50188886284826,27.24879209798205,66.07835052916674,True
full_unknown,add,emotion_minus_matched_random,raw_effect_pp,0.05261474999588509,-0.2760040055896453,0.3803008147214332,True

```

## 감정 축 타당성과 해석 범위

```json
{
  "7B": {
    "development_lofo": {
      "n": 320,
      "accuracy": 0.95,
      "fear_recall": 1.0,
      "recall": {
        "panic": 0.975,
        "fear": 1.0,
        "anxiety": 0.85,
        "desperation": 0.975,
        "sadness": 0.925,
        "anger": 0.975,
        "joy": 0.925,
        "calm": 0.975
      },
      "topics": 40,
      "families": 16
    },
    "legacy_heldout": {
      "n": 160,
      "accuracy": 0.475,
      "fear_recall": 0.45,
      "recall": {
        "panic": 0.85,
        "fear": 0.45,
        "anxiety": 0.2,
        "desperation": 0.0,
        "sadness": 0.2,
        "anger": 0.45,
        "joy": 0.75,
        "calm": 0.9
      },
      "topics": 20,
      "families": 10,
      "no_refitting": true,
      "previously_used_legacy_evaluation": true
    }
  },
  "14B": {
    "development_lofo": {
      "n": 320,
      "accuracy": 0.965625,
      "fear_recall": 1.0,
      "recall": {
        "panic": 1.0,
        "fear": 1.0,
        "anxiety": 0.925,
        "desperation": 0.975,
        "sadness": 0.95,
        "anger": 0.975,
        "joy": 0.95,
        "calm": 0.95
      },
      "topics": 40,
      "families": 16
    },
    "legacy_heldout": {
      "n": 160,
      "accuracy": 0.5,
      "fear_recall": 0.55,
      "recall": {
        "panic": 0.9,
        "fear": 0.55,
        "anxiety": 0.2,
        "desperation": 0.0,
        "sadness": 0.25,
        "anger": 0.4,
        "joy": 0.75,
        "calm": 0.95
      },
      "topics": 20,
      "families": 10,
      "no_refitting": true,
      "previously_used_legacy_evaluation": true
    }
  }
}
```

감정성분은지정된8축공간에투영된성분이다. 잔차를비감정으로명명하지않는다. 개발LOFO와과거legacy20주제평가를구분한다. 전체방향d의제거·재현포착률이낮으면감정비중의나머지를잔차로돌리지않는다. 무작위대조는감정norm의20방향이며잔차특이성을검증하는대조는없다.

14B비교가끝났으며자동확장하지않고다음지시를기다린다.
