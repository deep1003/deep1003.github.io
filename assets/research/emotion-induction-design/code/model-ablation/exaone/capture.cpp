#include "arg.h"
#include "common.h"
#include "llama.h"
#include <fstream>
#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
#include <algorithm>
#include "ggml-backend.h"
static std::string hidden_path;
static bool capture(struct ggml_tensor*t,bool ask,void*){
 bool selected=std::string(t->name)=="l_out-15";if(ask)return selected;if(!selected)return true;if(t->type!=GGML_TYPE_F32)return false;std::vector<float>data(ggml_nbytes(t)/4);ggml_backend_tensor_get(t,data.data(),0,ggml_nbytes(t));std::ofstream out(hidden_path+".bin",std::ios::binary);out.write((const char*)data.data(),ggml_nbytes(t));std::ofstream shape(hidden_path+".shape");for(int i=0;i<4;i++)shape<<t->ne[i]<<" ";return true;}
int main(int argc,char**argv){
 common_params p;common_init();if(!common_params_parse(argc,argv,p,LLAMA_EXAMPLE_COMMON))return 1;p.warmup=false;p.cb_eval=capture;llama_backend_init();auto init=common_init_from_params(p);auto*ctx=init->context();auto*model=init->model();if(!ctx||!model)return 2;const auto*vocab=llama_model_get_vocab(model);const int n=llama_vocab_n_tokens(vocab);std::vector<int>ids;
 for(int i=1;i<=3;i++){auto v=common_tokenize(ctx,std::to_string(i),false,true);if(v.size()!=1)return 3;ids.push_back(v[0]);}
 std::string path;std::cout<<std::setprecision(17);
 while(std::getline(std::cin,path)){
  std::ifstream f(path);if(!f)return 4;std::string text((std::istreambuf_iterator<char>(f)),{});llama_memory_clear(llama_get_memory(ctx),true);auto tokens=common_tokenize(ctx,text,llama_vocab_get_add_bos(vocab),true);if(tokens.empty()||tokens.size()>512)return 5;
  hidden_path=path;common_batch batch=common_batch_get_one(ctx,tokens);if(llama_process(ctx,LLAMA_PROCESS_TYPE_DECODE,batch.get()))return 6;const float*l=llama_get_logits_ith(ctx,-1);if(!l)return 7;double mx=-std::numeric_limits<double>::infinity();for(int i=0;i<n;i++){if(!std::isfinite(l[i]))return 8;mx=std::max(mx,(double)l[i]);}double total=0;for(int i=0;i<n;i++)total+=std::exp(l[i]-mx);double lse=mx+std::log(total);
  std::cout<<"{\"n_tokens\":"<<tokens.size()<<",\"vocab_size\":"<<n<<",\"ids\":["<<ids[0]<<","<<ids[1]<<","<<ids[2]<<"],\"logits\":["<<l[ids[0]]<<","<<l[ids[1]]<<","<<l[ids[2]]<<"],\"full_logsumexp\":"<<lse<<",\"all_vocab_finite\":true,\"pieces_hex\":[";
 for(size_t j=0;j<tokens.size();j++){char buf[2048];int len=llama_token_to_piece(vocab,tokens[j],buf,sizeof(buf),0,true);if(len<0)return 9;if(j)std::cout<<",";std::cout<<"\"";static const char*hex="0123456789abcdef";for(int k=0;k<len;k++){unsigned char v=buf[k];std::cout<<hex[v>>4]<<hex[v&15];}std::cout<<"\"";}std::cout<<"]}"<<std::endl;
 }
 return 0;
}
