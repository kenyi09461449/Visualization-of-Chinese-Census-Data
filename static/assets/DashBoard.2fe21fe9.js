import{a as N,u as S,b as O,s as H,y as R,c as t,o as s,e as v,F as y,z as I,t as c,h as e,g as o,B as w,f as r,v as k,A as $,_ as V,x as b,l as D,p as z,m as P}from"./index.794eb616.js";import{_ as U}from"./logo.09271933.js";const A={class:"navMenu"},j={slot:"title"},G={__name:"Menu",props:["navMenus"],setup(i){const u=i,_=N(),f=S(),m=O([]),h=(p,l)=>{_.push(p),f.state.tagName=l};return H(()=>{m.value=u.navMenus}),R(()=>u.navMenus,()=>{m.value=u.navMenus}),(p,l)=>{const d=t("el-icon"),g=t("el-menu-item"),x=t("el-sub-menu");return s(),v("div",A,[(s(!0),v(y,null,I(m.value,n=>(s(),v(y,null,[n.children?$("",!0):(s(),c(g,{key:n.id,index:n.name,onClick:a=>h(n.name,n.alias)},{default:e(()=>[o(d,null,{default:e(()=>[(s(),c(w(n.icon)))]),_:2},1024),r("span",j,k(n.alias),1)]),_:2},1032,["index","onClick"])),n.children?(s(),c(x,{key:1,index:n.name},{title:e(()=>[o(d,null,{default:e(()=>[(s(),c(w(n.icon)))]),_:2},1024),r("span",null,k(n.alias),1)]),default:e(()=>[(s(!0),v(y,null,I(n.children,a=>(s(),c(g,{index:a.name,onClick:C=>h(a.name,a.alias)},{default:e(()=>[o(d,null,{default:e(()=>[(s(),c(w(a.icon)))]),_:2},1024),r("span",null,k(a.alias),1)]),_:2},1032,["index","onClick"]))),256))]),_:2},1032,["index"])):$("",!0)],64))),256))])}}},T={root:[{id:1,name:"/user",icon:"User",alias:"User"},{id:2,name:"/age",icon:"Document",alias:"AgeData"},{id:3,name:"/birth",icon:"Document",alias:"BirthData"},{id:4,name:"/gdp",icon:"Document",alias:"GdpData"},{id:5,name:"/people",icon:"Document",alias:"PeopleData"},{id:6,name:"/province",icon:"Document",alias:"ProvinceData"}]};const Y=i=>(z("data-v-57b47774"),i=i(),P(),i),q={class:"header-container"},J=Y(()=>r("div",{class:"logo-img"},[r("img",{src:U})],-1)),K=[J],Q={key:0,class:"btn-group"},W={class:"login"},X={class:"register"},Z={key:1,class:"btn-group"},ee={__name:"Header",setup(i){const u=N(),_=S(),f=p=>{u.push({name:p})},m=()=>{console.log("userinfo",_.state.user),_.state.user||u.push({name:"Login"})},h=()=>{_.commit("REMOVE_INFO"),u.push("/")};return H(()=>{m()}),(p,l)=>{const d=t("el-button"),g=t("Bell"),x=t("el-icon"),n=t("el-text"),a=t("el-popover"),C=t("el-avatar"),E=t("el-dropdown-item"),F=t("el-dropdown-menu"),M=t("el-dropdown"),L=t("el-header");return s(),c(L,{class:"header"},{default:e(()=>[r("div",q,[r("div",{class:"logo",onClick:l[0]||(l[0]=B=>f("Home"))},K),b(_).state.user?(s(),v("div",Z,[b(_).state.user.role===1?(s(),c(a,{key:0,placement:"bottom",width:300,trigger:"click"},{reference:e(()=>[o(n,{class:"welcome"},{default:e(()=>[o(x,{size:"22"},{default:e(()=>[o(g)]),_:1})]),_:1})]),_:1})):$("",!0),o(M,null,{dropdown:e(()=>[o(F,null,{default:e(()=>[o(E,{onClick:h},{default:e(()=>[D("Sign out")]),_:1})]),_:1})]),default:e(()=>[o(C,{size:50},{default:e(()=>[D(k(b(_).getters.getUser.username),1)]),_:1})]),_:1})])):(s(),v("div",Q,[r("div",W,[o(d,{type:"primary",onClick:l[1]||(l[1]=B=>f("Login"))},{default:e(()=>[D("Log in")]),_:1})]),r("div",X,[o(d,{onClick:l[2]||(l[2]=B=>f("Register"))},{default:e(()=>[D("Sign up")]),_:1})])]))])]),_:1})}}},te=V(ee,[["__scopeId","data-v-57b47774"]]);const oe={name:"DashBoard",components:{Header:te,Menu:G},data(){return{menuData:[],year:new Date().getFullYear()}},mounted(){this.menuData=T.root},methods:{logout(){this.$store.commit("REMOVE_INFO"),this.$router.push("/login")}}};function ne(i,u,_,f,m,h){const p=t("Header"),l=t("Menu"),d=t("el-menu"),g=t("el-aside"),x=t("router-view"),n=t("el-main"),a=t("el-container");return s(),c(a,{class:"el-container-fix"},{default:e(()=>[o(p),o(a,null,{default:e(()=>[o(g,{width:"250px",class:"el-aside"},{default:e(()=>[o(d,{"default-active":i.$route.path,"background-color":"#fff","text-color":"#312f2fd4","text-align":"left","active-text-color":"#fff"},{default:e(()=>[o(l,{navMenus:m.menuData},null,8,["navMenus"])]),_:1},8,["default-active"])]),_:1}),o(a,null,{default:e(()=>[o(n,null,{default:e(()=>[o(x)]),_:1})]),_:1})]),_:1})]),_:1})}const le=V(oe,[["render",ne],["__scopeId","data-v-ba1aa5d0"]]);export{le as default};
