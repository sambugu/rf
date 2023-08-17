// The Soil-Plant-Atmosphere Remote Sensing of Evapotranspiration - SPARSE JavaScript implementation
// -- ufu --

function runSP() {
	// INPUT data
	// surface temperature
	let Tsurf 	= document.getElementById("surf_Temp").value - 0; 			//or *1
	//var Ts 		= document.getElementById("surf_Temp").value - 0; 		//or *1
	let vza 	= document.getElementById("view_zenith").value - 0;
	// meteorological data
	let rg 		= document.getElementById("solar_rad").value - 0;
	let Ta 		= document.getElementById("air_Temp").value - 0;
	let rh 		= document.getElementById("rel_Hum").value - 0;
	let ua 		= document.getElementById("wind_speed").value - 0;
	let za 		= document.getElementById("meas_height").value - 0;
	// biophysical parameters/variables and other ancillary data
	let lai 	= document.getElementById("lai").value - 0;
	let glai 	= lai; 														// green leaf area index - load correct data accordingly OTHERWISE ==lai
	let zf 		= document.getElementById("veg_height").value - 0;
	let rstmin 	= document.getElementById("min_stomres").value - 0;
	let albv 	= document.getElementById("veg_alb").value - 0;
	let emisv 	= document.getElementById("veg_emis").value - 0;
	let emiss 	= document.getElementById("soil_emis").value - 0;
	let emissf 	= document.getElementById("surf_emis").value - 0;
	
	let albe 	= document.getElementById("surf_albedo").value - 0;
	let xg 		= document.getElementById("max_GRns").value - 0;
	let sigmoy 	= document.getElementById("fol_prjfactor").value - 0;
	
	let albmode = document.getElementById("albmode").value;

	[LE,H,Rn,G,LEv,LEs,Hv,Hs,Tv,Ts,Tsf] = SPARSE(Tsurf,vza,rg,Ta,rh,ua,za,lai,glai,zf,rstmin,albv,emisv,emiss,emissf,albe,xg,sigmoy,albmode);
	//var SEB_output = document.getElementById('output');
	//SEB_output.innerHTML = [le,h,rn,g,lev,les,hv,hs,tv,ts,tsf];
	SEB_output.textContent = ["LE : "+LE,"H : "+H,"Rn : "+Rn,"G : "+G,LEv,LEs,Hv,Hs,Tv,Ts,Tsf];
}

/* SPARSE evapotranspiration algorithm - Boulet et al. (2015) - [https://gitlab.cesbio.omp.eu/bouletg/sparse : matlab scripts]
Soil-Plant-Atmosphere Remote Sensing of Evapotranspiration
	A surface energy balance method for the estimation and partioning
	of turbulent fluxes (latent and sensible energy) at the 
	near-land surface
	
        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
	
-- ufu -- translated to JS from 160623
*/

//function [tsurf,tvs,tvh,tgs,tgh,t0,rns,rnv,g,hs,hv,h,les,lev,le,betavs,rtmdat] = 
//SPARSE4(betas,betav,vza,vaa,sunangles,albe,tsobs,ta,rh,rg,ua,glai,lai,cvr,zf,za,rvvmin,XG,sigmoy)
	
function SPARSE(Tsurf,vza,rg,Ta,rh,ua,za,lai,glai,zf,rstmin,albv,emisv,emiss,emissf,albe,xg,sigmoy,albmode){

/*	
// INPUT data
// surface temperature
let Tsurf 	= document.getElementById("surf_Temp").value - 0; 			//or *1
//var Ts 		= document.getElementById("surf_Temp").value - 0; 		//or *1
let vza 	= document.getElementById("view_zenith").value - 0;
// meteorological data
let rg 		= document.getElementById("solar_rad").value - 0;
let Ta 		= document.getElementById("air_Temp").value - 0;
let rh 		= document.getElementById("rel_Hum").value - 0;
let ua 		= document.getElementById("wind_speed").value - 0;
let za 		= document.getElementById("meas_height").value - 0;
// biophysical parameters/variables and other ancillary data
let lai 	= document.getElementById("lai").value - 0;
let glai 	= lai; 														// green leaf area index - load correct data accordingly OTHERWISE ==lai
let zf 		= document.getElementById("veg_height").value - 0;
let rstmin 	= document.getElementById("min_stomres").value - 0;
let albv 	= document.getElementById("veg_alb").value - 0;
let emisv 	= document.getElementById("veg_emis").value - 0;
let emiss 	= document.getElementById("soil_emis").value - 0;
let emissf 	= document.getElementById("surf_emis").value - 0;

let albe 	= document.getElementById("surf_albedo").value - 0;
let xg 		= document.getElementById("max_GRns").value - 0;
let sigmoy 	= document.getElementById("fol_prjfactor").value - 0;

let albmode = document.getElementById("albmode").value;
*/

// constants
const rcp 	= 1170;
const gamma = 0.66;
const sigma = 5.67e-8;
const alfo 	= 0.005;
const xn 	= 2.5;
const zoms 	= 0.005;
const wl 	= 0.1;

const albsmn= 0.1;const albsmx= 0.5; //maybe shld not be hardcoded ??

// partial pressure [ea], apparent emissivity [emisa], and sky radiance [ratm]
let ea		= 0.01*rh*6.11*(Math.E**(17.269*(Ta-273.15)/(Ta-35.85)));
let emisa	= 1.24*((ea/Ta)**(1/7));
let ratm	= emisa*sigma*(Ta**4);
//related terms appearing in the [Taylor] SEB linearization
let da		= 6.11*(Math.E**(17.269*(Ta-273.15)/(Ta-35.85))) - ea;
let delta	= ((da+ea)*4097.9337)*((Ta-35.85)**(-2));
let rcpg	= rcp/gamma;
let rcpgd	= rcpg*delta;

// vegetation fraction cover - nadir and at view angle of the tir sensor
let fcov	= 1 - Math.E**(-sigmoy*lai/Math.cos(0));
let fcovl 	= fcov;									// ???
var fcov_vz	= 1 - Math.E**(-sigmoy*lai/Math.cos(vza));

// roughness length zoms and displacement height data
let d		= 0.66*zf;
let zom 	= Math.max(zoms,0.13*zf);
//soil-air aerodynamic resistance/conductance
let xkzf	= 0.4*0.4*ua*(zf-d)/Math.log((za-d)/zom);
let ras		= zf*(Math.E**xn)*((Math.E**(-xn*zoms/zf))-(Math.E**((-xn*(d+zom))/zf)))/(xn*xkzf);
// leaf-air aerodynamic resistance/conductance
let uzf		= ua*Math.log((zf-d)/zom)/Math.log((za-d)/zom);
let rav		= xn*Math.sqrt(wl/uzf)/(4*alfo*glai*(1-Math.E**(-xn/2)));
// leaf-air stomatal conductance
let f 		= (0.0055*Math.max(rg,10)*2)/glai;
let frg 	= (1+f)/(f+rstmin/5000);
let fea 	= 1 + 0.04*da;
// aerodynamic resistance in neutral conditions
let alg 	= Math.log((za-d)/zom);
let ra0 	= alg*alg/(0.4*0.4*ua);


//radiation forcing terms - layer/series approach
let [albs,ans,bns,cns,anv,bnv,cnv,cnas,cnav] = calcRn(rg,ratm,emiss,emisv,albe,albv,fcov,fcovl,albsmn,albsmx,albmode);
let arns 	= (ans*sigma*4*(Ta**3))*(1-xg);
let aras 	= ans*sigma*4*(Ta**3);
let brns 	= (bns*sigma*4*(Ta**3))*(1-xg);
let bras 	= bns*sigma*4*(Ta**3);
let arnv 	= anv*sigma*4*(Ta**3);
let arav 	= arnv;
let brnv 	= bnv*sigma*4*(Ta**3);
let brav 	= brnv;
let crns 	= ((ans+bns)*sigma*(Ta**4) + cns)*(1-xg);
let crnv 	= (anv+bnv)*sigma*(Ta**4) + cnv;
let cras 	= (ans+bns)*sigma*(Ta**4) + cnas;
let crav 	= (anv+bnv)*sigma*(Ta**4) + cnav;

let Mrad 	= (1-emissf)*ratm + emissf*sigma*Tsurf**4;

//initialization
X0 			= 5; X0old = X0;
errSEB 		= 10;
k 			= 0;
LEsmin 		= 0; LEvmin = 0;

//stability loop
while (errSEB > 0.01 && k < 100){
	k += 1;
	// air-air aerodynamic conductance
	// Richardson Number
	ri 		= 5*(za-d)*9.81*X0/(ua*ua*Ta);
	if (rg < 100){
		ri 	= 0;
	}
	
	if (X0 > 0){
		p 	= 0.75; 													// unstable conditions
	} else {
		p 	= 2; 														// stable conditions
	}
	
	ra 		= ra0/((1+ri)**p);
	ga 		= 1/ra;
	// aggregated conductances for series/layer approach
	gav 	= 1/rav;
	gvv 	= 1/(rstmin*fea*frg/glai + rav);
	gas 	= 1/ras;
	gss 	= 1/ras;
	g3a 	= ga + gas + gav;
	g3 		= ga + gss + gvv;
	
	// solving the SEB [EB coefficients, coefficient matrix (LHS), and the RHS of the augmented matrix]
		//LHS
	A1_1 	= 1;
	A1_2 	= -rcp*gas*gas/g3a - arns + rcp*gas;
	A1_3 	= -rcp*gas*gav/g3a - brns;
	A2_1 	= -gvv/(gvv+ga);
	A2_2 	= -rcp*gav*gas/g3a - arnv;
	A2_3 	= -rcpgd*gvv*gvv/(gvv+ga) - rcp*gav*gav/g3a + rcpgd*gvv + rcp*gav - brnv;
	//linking observed Tsurf with the source temperatures
	A3_1 	= 0;
	A3_2 	= -aras - arav;
	A3_3 	= -bras-brav;
		//RHS
	B1 		= crns;
	B2 		= crnv - rcpg*gvv*ga*da/(gvv+ga);
	B3 		= Mrad + cras + crav - ratm;
	// SEB matrix solution [A|B] ; [X]=Inv[A][B]
	[X1,X2,X3] = SEBsoln(A1_1,A1_2,A1_3,A2_1,A2_2,A2_3,A3_1,A3_2,A3_3,B1,B2,B3);

	// output
	X0 		= (gas*X2 + gav*X3)/g3a;
	d0 		= (rcpg*ga*da - X1 - rcpgd*gvv*X3)/(rcpg*(gvv+ga));
	LEs 	= X1;
	LEv		= rcpg*gvv*(d0 + delta*X3);
		
	if (LEs < LEsmin){
			//LHS
		A1_1 		= 0;
		A1_2 		= -rcp*gas*gas/g3a - arns + rcp*gas;
		A1_3 		= -rcp*gas*gav/g3a - brns;
		A2_1 		= 1;
		A2_2 		= -rcp*gav*gas/g3a - arnv;
		A2_3 		= -rcp*gav*gav/g3a + rcp*gav - brnv;
		//linking observed Tsurf with the source temperatures
		A3_1 		= 0;
		A3_2 		= -aras - arav;
		A3_3 		= -bras - brav;
			//RHS
		B1 			= crns - LEsmin;
		B2 			= crnv;
		B3 			= Mrad + cras + crav - ratm;
		
		// SEB matrix solution [A|B] ; [X]=Inv[A][B]
			// X1 = LEv; X2 = Ts-Ta; X3 = Tv-Ta;
		[X1,X2,X3] 	= SEBsoln(A1_1,A1_2,A1_3,A2_1,A2_2,A2_3,A3_1,A3_2,A3_3,B1,B2,B3);
		
		// output
		X0 			= (gas*X2 + gav*X3)/g3a;
		d0 			= da - (LEsmin + X1)/(rcpg*ga);
		LEv 		= X1; LEs = LEsmin;
		
		if (LEv < LEvmin){
				//LHS
			A1_1 	= -rcp*gas*gas/g3a - arns + rcp*gas;
			A1_2 	= -rcp*gas*gav/g3a - brns;
			A2_1 	= -rcp*gav*gas/g3a - arnv;
			A2_2 	= -rcp*gav*gav/g3a + rcp*gav - brnv;
				//RHS
			B1 		= crns - LEsmin;
			B2 		= crnv;
			
			// SEB matrix solution [A|B] ; [X]=Inv[A][B]
				// X2 = Ts-Ta; X3 = Tv-Ta;
			detA 	= A1_1*A2_2 - A1_2*A2_1;
			X2 		= (1/detA)*(A2_2*B1 - A1_2*B2);
			X3 		= (1/detA)*(-A2_1*B1 + A1_1*B2);
			// output
			X0 		= (gas*X2 + gav*X3)/g3a;
			d0 		= (ga*da - gss*delta*X2 - gvv*delta*X3)/g3;
			LEv 	= LEvmin; LEs = LEsmin;
		}
	}
	
	//convergence checks
	errSEB 			= Math.abs(X0 - X0old);	Xold = X0;
	if (rg < 20){
		errSEB 		= 0.001;
	}
	
} // end stability loop

// other SEB outputs - fluxes and temperatures
let rns 	= (crns + arns*X2 + brns*X3)/(1-xg);
let rnv 	= (crnv + arnv*X2 + brnv*X3);
let rn 		= rns + rnv;

let Hs 		= rcp*gas*(X2-X0); 											// soil sensible heat
let Hv 		= rcp*gav*(X3-X0); 											// vegetation sensible heat
let H 		= Hs + Hv; 													// overall sensible heat flux
let LE		= LEs + LEv;												// overall latent heat energy
let G 		= xg*rns;

let T0 		= X0 + Ta; 													// aerodynamic temperature in [K]
let Ts 		= X2 + Ta; 													// soil temperature in [K]
let Tv 		= X3 + Ta;	 												// vegetation temperature in [K]
let Tsf 	= ((emissf*ratm - cras - crav - X2*(aras+arav) - X3*(bras+brav))/(sigma*emissf))**0.25; 

//document.getElementById("SEB_output").innerHTML = [Math.floor(LE),Math.floor(H),Math.floor(rn),Math.floor(G),Math.floor(LEv),Math.floor(LEs),Math.floor(Hv),Math.floor(Hs),Math.floor(Tv),Math.floor(Ts),Math.floor(Tsf)];
return [Math.floor(LE),Math.floor(H),Math.floor(rn),Math.floor(G),Math.floor(LEv),Math.floor(LEs),Math.floor(Hv),Math.floor(Hs),Math.floor(Tv),Math.floor(Ts),Math.floor(Tsf)];
//return [LE,H,Rn,G,LEv,LEs,Hv,Hs,Tv,Ts,Tsf];
}

function calcRn(rg,ratm,emiss,emisv,albe,albv,fcov,fcovl,albsmn,albsmx,albmode){
	// calculate rn forcing terms
	if (albmode != 'Capped'){
		var albs 	= (albe-fcov*albv)/((1-fcov)**2 + fcov*albv*albe - (fcov*albv)**2);
	} else {
		var albs 	= Math.max(albsmn,Math.min(albsmn,(albe-fcov*albv)/((1-fcov)**2 + fcov*albv*albe - (fcov*albv)**2)));		
	}
	//var albs 	= (albe-fcov*albv)/((1-fcov)**2 + fcov*albv*albe - (fcov*albv)**2);
	//var albs 	= Math.max(albsmn,Math.min(albsmn,(albe-fcov*albv)/((1-fcov)**2 + fcov*albv*albe - (fcov*albv)**2)));
	v1 			= 1 - albv*albs*fcov; 	v1a = 1 - albv*albs*fcovl;
	v2 			= 1 - emisv;
	v3 			= 1 - emiss;
	v4 			= 1 - fcov; 			v4a = 1 - fcovl;
	v5 			= 1 - fcov*v2*v3; 		v5a = 1 - fcovl*v2*v3;
	var arns 	= -(v4a*emiss + emisv*emiss*fcovl)/v5a;
	var brns 	= (emisv*emiss*fcovl)/v5a;
	var crns 	= (rg*(1-albs)*v4)/v1 + (v4a*emiss*ratm)/v5a;
	var cras 	= (v4a*emiss*ratm)/v5a;
	var arnv 	= brns;
	var brnv 	= -fcovl*(emisv + (emisv*emiss + v4a*v3*emisv)/v5a);
	var crnv 	= rg*(1-albv)*fcov*(1 + (albs*v4)/v1) + fcovl*emisv*ratm*(1 + (v4a*v3)/v5a);
	var crav 	= fcovl*emisv*ratm*(1 + (v4a*v3)/v5a);

	return [albs,arns,brns,crns,arnv,brnv,crnv,cras,crav];
}

function SEBsoln(A1_1,A1_2,A1_3,A2_1,A2_2,A2_3,A3_1,A3_2,A3_3,B1,B2,B3){
	// SEB matrix solution [A|B] ; [X]=Inv[A][B]
		//determinant of A
	detA 	= A1_1*(A2_2*A3_3-A2_3*A3_2) - A1_2*(A2_1*A3_3-A2_3*A3_1) + A1_3*(A2_1*A3_2-A2_2*A3_1);	
		//inverse matrix coefficients
	IA1_1	=  (A2_2*A3_3 - A2_3*A3_2)/detA;
	IA1_2	= -(A1_2*A3_3 - A1_3*A3_2)/detA;
	IA1_3	=  (A1_2*A2_3 - A1_3*A2_2)/detA;
	IA2_1	= -(A2_1*A3_3 - A2_3*A3_1)/detA;
	IA2_2	=  (A1_1*A3_3 - A1_3*A3_1)/detA;
	IA2_3	= -(A1_1*A2_3 - A1_3*A2_1)/detA;
	IA3_1	=  (A2_1*A3_2 - A2_2*A3_1)/detA;
	IA3_2	= -(A1_1*A3_2 - A1_2*A3_1)/detA;
	IA3_3	=  (A1_1*A2_2 - A1_2*A2_1)/detA;
		// solution
	var X1 	= IA1_1*B1 + IA1_2*B2 + IA1_3*B3; //LEs or LEv
	var X2 	= IA2_1*B1 + IA2_2*B2 + IA2_3*B3; //Ts-Ta
	var X3 	= IA3_1*B1 + IA3_2*B2 + IA3_3*B3; //Tv-Ta
	
	return [X1,X2,X3];
}

//--uΓu--
