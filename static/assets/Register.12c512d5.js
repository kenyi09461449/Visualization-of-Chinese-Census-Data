import{_ as q,u as L,a as Z,r as B,b as h,c as l,d as K,o as w,e as y,w as M,n as O,f as n,g as o,h as s,F as Y,i as j,k as R,j as $,l as V,p as G,m as H,E as b}from"./index.794eb616.js";import{_ as J}from"./bg.79b7f3df.js";import{a as Q}from"./user.f7bb43e6.js";import"./request.e71a236e.js";const _=p=>(G("data-v-f3572491"),p=p(),H(),p),W=j('<video src="'+J+'" class="bg-video" muted loop autoplay data-v-f3572491></video><div class="left-title" data-v-f3572491><h1 class="main-title" data-v-f3572491>POPULATION DATA ANALYSIS</h1><h3 class="main-desc" data-v-f3572491><a href="https://data.stats.gov.cn/" data-v-f3572491>Data from https://data.stats.gov.cn/</a></h3></div>',2),X={class:"left-right"},ee=_(()=>n("div",{class:"title-container"},[n("h3",{class:"app-title"},"Register")],-1)),oe={class:"more-options"},te={class:"more-options-left"},se=_(()=>n("div",{class:"no-account-tips"},"Registered?",-1)),ae=_(()=>n("div",{class:"more-options-right"},null,-1)),re={__name:"Register",setup(p){L();const x=Z(),a=B({username:"",password:"",repeatpassword:"",email:""}),E=(r,e,t)=>{e?t():t(new Error("Please enter your username"))},P=(r,e,t)=>{e.length<6?t(new Error("The password can not be less than 6 digits")):t()},I=(r,e,t)=>{e.length<6?t(new Error("The password can not be less than 6 digits")):e!==a.password?t(new Error("The two input passwords do not match!")):t()},z=(r,e,t)=>{e?/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/.test(e)?t():t(new Error("Please enter a valid email address")):t(new Error("Please enter your email"))},A=(r,e,t)=>{e?t():t(new Error("Please enter your phone"))},f=h(null),F=r=>{f.value.validate(e=>{e?r():console.log("error submit!!")})},S={username:[{required:!0,trigger:"blur",validator:E}],password:[{required:!0,trigger:"blur",validator:P}],repeatpassword:[{required:!0,trigger:"blur",validator:I}],email:[{required:!0,trigger:"blur",validator:z}],phone:[{required:!0,trigger:"blur",validator:A}]},u=h(!1);new Date().getFullYear();const g=()=>{F(()=>{u.value=!0;let r={...a};Q(r).then(e=>{u.value=!1,e.code===200?(b.success("Register successful!"),x.push({name:"login"})):b.error(e.msg)}).catch(e=>{console.error(e),u.value=!1})})};return(r,e)=>{const t=l("User"),c=l("el-icon"),m=l("el-input"),d=l("el-form-item"),v=l("Lock"),U=l("ChatDotRound"),D=l("el-button"),C=l("el-link"),N=l("el-form"),T=l("Footer"),k=K("loading");return w(),y(Y,null,[M((w(),y("div",{"element-loading-text":"loading","element-loading-spinner":"el-icon-loading","element-loading-background":"rgba(0, 0, 0, 0.6)",class:"login-container",style:O(r.bg)},[W,n("div",X,[o(N,{ref_key:"registerFormRef",ref:f,model:a,rules:S,class:"login-form","auto-complete":"on","label-position":"left"},{default:s(()=>[ee,o(d,{prop:"username"},{default:s(()=>[o(m,{modelValue:a.username,"onUpdate:modelValue":e[0]||(e[0]=i=>a.username=i),placeholder:"Username",size:"large",tabIndex:"-1"},{prefix:s(()=>[o(c,{class:"el-input__icon"},{default:s(()=>[o(t)]),_:1})]),_:1},8,["modelValue"])]),_:1}),o(d,{prop:"password"},{default:s(()=>[o(m,{ref:"password",modelValue:a.password,"onUpdate:modelValue":e[1]||(e[1]=i=>a.password=i),size:"large","show-password":"",placeholder:"Password",name:"password",tabIndex:"-1","auto-complete":"on"},{prefix:s(()=>[o(c,{class:"el-input__icon"},{default:s(()=>[o(v)]),_:1})]),_:1},8,["modelValue"])]),_:1}),o(d,{prop:"repeatpassword"},{default:s(()=>[o(m,{ref:"repeatpassword",modelValue:a.repeatpassword,"onUpdate:modelValue":e[2]||(e[2]=i=>a.repeatpassword=i),size:"large","show-password":"",placeholder:"Repeat Password",name:"password",tabIndex:"-1","auto-complete":"on"},{prefix:s(()=>[o(c,{class:"el-input__icon"},{default:s(()=>[o(v)]),_:1})]),_:1},8,["modelValue"])]),_:1}),o(d,{prop:"email"},{default:s(()=>[o(m,{ref:"email",modelValue:a.email,"onUpdate:modelValue":e[3]||(e[3]=i=>a.email=i),size:"large",placeholder:"Email",name:"email",tabIndex:"-1","auto-complete":"on"},{prefix:s(()=>[o(c,{class:"el-input__icon"},{default:s(()=>[o(U)]),_:1})]),_:1},8,["modelValue"])]),_:1}),o(d,null,{default:s(()=>[o(D,{type:"primary",class:"login-btn",onClick:R(g,["prevent"]),onKeyup:$(R(g,["prevent"]),["enter"])},{default:s(()=>[V(" Sign up ")]),_:1},8,["onClick","onKeyup"])]),_:1}),n("div",oe,[n("div",te,[se,n("div",null,[o(C,{underline:!1,type:"primary",href:"#/login"},{default:s(()=>[V("Log in")]),_:1})])]),ae])]),_:1},8,["model"])])],4)),[[k,u.value,void 0,{fullscreen:!0,lock:!0}]]),o(T,{class:"footer"})],64)}}},pe=q(re,[["__scopeId","data-v-f3572491"]]);export{pe as default};
