import{A as D,k as h,D as v,R as k,f as u,F as C,G as w,H as x,g as t,w as l,L as B,h as r,o as c,j as y,l as n,t as U,E as F,Q as f}from"./vendor.69764f60.js";const A={name:"InsertImage",props:["editor"],expose:["openDialog"],data(){return{addVideoDialog:{url:"",file:null,show:!1}}},components:{Button:h,Dialog:v,FileUploader:k},methods:{openDialog(){this.addVideoDialog.show=!0},onVideoSelect(i){let o=i.target.files[0];!o||(this.addVideoDialog.file=o)},addVideo(i){this.editor.chain().focus().insertContent(`<video src="${i}"></video>`).run(),this.reset()},reset(){this.addVideoDialog=this.$options.data().addVideoDialog}}},I={class:"flex items-center space-x-2"},N=n(" Remove "),S=["src"],L=n(" Insert Video "),R=n("Cancel");function j(i,o,E,P,e,s){const a=r("Button"),g=r("FileUploader"),p=r("Dialog");return c(),u(B,null,[C(i.$slots,"default",w(x({onClick:s.openDialog}))),t(p,{options:{title:"Add Video"},modelValue:e.addVideoDialog.show,"onUpdate:modelValue":o[2]||(o[2]=d=>e.addVideoDialog.show=d),onAfterLeave:s.reset},{"body-content":l(()=>[t(g,{"file-types":"video/*",onSuccess:o[0]||(o[0]=d=>e.addVideoDialog.url=d.file_url)},{default:l(({file:d,progress:V,uploading:_,openFileSelector:m})=>[y("div",I,[t(a,{onClick:m},{default:l(()=>[n(U(_?`Uploading ${V}%`:e.addVideoDialog.url?"Change Video":"Upload Video"),1)]),_:2},1032,["onClick"]),e.addVideoDialog.url?(c(),F(a,{key:0,onClick:()=>{e.addVideoDialog.url=null,e.addVideoDialog.file=null}},{default:l(()=>[N]),_:2},1032,["onClick"])):f("",!0)])]),_:1}),e.addVideoDialog.url?(c(),u("video",{key:0,src:e.addVideoDialog.url,class:"mt-2 w-full rounded-lg",type:"video/mp4",controls:""},null,8,S)):f("",!0)]),actions:l(()=>[t(a,{variant:"solid",onClick:o[1]||(o[1]=d=>s.addVideo(e.addVideoDialog.url))},{default:l(()=>[L]),_:1}),t(a,{onClick:s.reset},{default:l(()=>[R]),_:1},8,["onClick"])]),_:1},8,["modelValue","onAfterLeave"])],64)}var z=D(A,[["render",j]]);export{z as default};
