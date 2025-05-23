#======================================================================================================================================
#======================================================================================================================================
# SPARSE evapotranspiration model/algorithm - Boulet et al. (2015) - [https://gitlab.cesbio.omp.eu/bouletg/sparse : matlab scripts]
# Soil-Plant-Atmosphere Remote Sensing of Evapotranspiration : https://doi.org/10.5194/hess-19-4653-2015
#     A surface energy balance method for the estimation and partitioning
#     of turbulent fluxes (latent and sensible energy) at the 
#     near-land surface
#
#		.This is free software under the GNU General Public License v3.0.
#		.GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html
#		[tested - RStudio v2023.06.2]
#
# -- ufu -- translated to R from 180823
#======================================================================================================================================

# function [tsurf,tvs,tvh,tgs,tgh,t0,rns,rnv,g,hs,hv,h,les,lev,le,betavs,rtmdat] = 
# SPARSE4(betas,betav,vza,vaa,sunangles,albe,tsobs,ta,rh,rg,ua,glai,lai,cvr,zf,za,rvvmin,XG,sigmoy)

rm(list=ls(all=TRUE))   # clear workspace

SPARSE        <- function(Tsurf,vza,rg,Ta,rh,ua,za,lai,glai,zf,rstmin,albv,emisv,emiss,emissf,albe,xg,sigmoy,albmode){
# The SPARSE algorithm
  
  ### constants
  rcp 	      <- 1170
  gamma       <- 0.66
  sigma       <- 5.67e-8
  alfo 	      <- 0.005
  xn 	        <- 2.5
  zoms 	      <- 0.005
  wl 	        <- 0.1
  
  albsmn      <- 0.05;  albsmx <- 0.7
  
  # partial pressure [ea], apparent emissivity [emisa], and sky radiance [ratm]
  ea		      <- 0.01*rh*6.11*(exp(17.269*(Ta - 273.15)/(Ta - 35.85)))
  emisa	      <- 1.24*((ea/Ta)^(1/7))
  ratm	      <- emisa*sigma*(Ta^4)
  # related terms appearing in the [Taylor] SEB linearization
  da		      <- 6.11*(exp(17.269*(Ta - 273.15)/(Ta - 35.85))) - ea
  delta	      <- ((da + ea)*4097.9337)*((Ta - 35.85)^(-2))
  rcpg	      <- rcp/gamma
  rcpgd	      <- rcpg*delta
  
  # vegetation fraction cover - nadir and at view angle of the tir sensor
  fcov	      <- 1 - exp(-sigmoy*lai/cos(0))
  fcovl 	    <- fcov									        # ???
  fcov_vz	    <- 1 - exp(-sigmoy*lai/cos(vza))
  
  # roughness length zoms and displacement height data
  d		        <- 0.66*zf
  zom 	      <- max(zoms,0.13*zf)
  # soil-air aerodynamic resistance/conductance
  xkzf	      <- 0.4*0.4*ua*(zf - d)/log((za - d)/zom)
  ras		      <- zf*(exp(xn))*((exp(-xn*zoms/zf)) - (exp((-xn*(d + zom))/zf)))/(xn*xkzf)
  # leaf-air aerodynamic resistance/conductance
  uzf		      <- ua*log((zf - d)/zom)/log((za - d)/zom)
  rav		      <- xn*sqrt(wl/uzf)/(4*alfo*glai*(1 - exp(-xn/2)))
  # leaf-air stomatal conductance
  f 		      <- (0.0055*max(rg,10)*2)/glai
  frg 	      <- (1 + f)/(f + rstmin/5000)
  fea 	      <- 1 + 0.04*da
  # aerodynamic resistance in neutral conditions
  alg 	      <- log((za - d)/zom)
  ra0 	      <- alg*alg/(0.4*0.4*ua)
  
  # radiation forcing terms - layer/series approach
  varsRn      = calcRn(rg,ratm,emiss,emisv,albe,albv,fcov,fcovl,albsmn,albsmx,albmode)
  albs        <- varsRn$albs; ans <- varsRn$arns;  bns <- varsRn$brns;  cns <- varsRn$crns
  anv         <- varsRn$arnv; bnv <- varsRn$brnv; cnv <- varsRn$crnv;  cnas <- varsRn$cras; cnav <- varsRn$crav

  arns 	      <- (ans*sigma*4*(Ta^3))*(1 - xg)
  aras 	      <- ans*sigma*4*(Ta^3)
  brns 	      <- (bns*sigma*4*(Ta^3))*(1 - xg)
  bras 	      <- bns*sigma*4*(Ta^3)
  arnv 	      <- anv*sigma*4*(Ta^3)
  arav 	      <- arnv
  brnv 	      <- bnv*sigma*4*(Ta^3)
  brav 	      <- brnv
  crns 	      <- ((ans + bns)*sigma*(Ta^4) + cns)*(1 - xg)
  crnv 	      <- (anv + bnv)*sigma*(Ta^4) + cnv
  cras 	      <- (ans + bns)*sigma*(Ta^4) + cnas
  crav 	      <- (anv + bnv)*sigma*(Ta^4) + cnav
  
  Mrad 	      <- (1 - emissf)*ratm + emissf*sigma*Tsurf^4
  
  # initialization
  X0 		      <- 5; X0old <- X0
  errSEB 	    <- 10
  k 		      <- 0
  LEsmin 	    <- 0; LEvmin <- 0
  
  # stability loop
  while (errSEB > 0.01 && k < 100){
    k         <- k + 1
    
    # air-air aerodynamic conductance
    # Richardson Number
    ri 	      <- 5*(za - d)*9.81*X0/(ua*ua*Ta)
    if (rg < 100){
      ri      <- 0
    }
          
    if (X0 > 0){
      p       <- 0.75                                                                              # unstable conditions
    } else {
      p       <- 2                                                                                 # stable conditions
    }
    ra 	      <- ra0/((1 + ri)^p)
    ga 	      <- 1/ra
    # aggregated conductances for series/layer approach
    gav 	    <- 1/rav
    gvv 	    <- 1/(rstmin*fea*frg/glai + rav)
    gas 	    <- 1/ras
    gss 	    <- 1/ras
    g3a 	    <- ga + gas + gav
    g3 	      <- ga + gss + gvv
    
    # solving the SEB [EB coefficients, coefficient matrix (LHS), and the RHS of the augmented matrix]
      # LHS
    A1_1 	    <- 1
    A1_2 	    <- -rcp*gas*gas/g3a - arns + rcp*gas
    A1_3 	    <- -rcp*gas*gav/g3a - brns
    A2_1 	    <- -gvv/(gvv+ga)
    A2_2 	    <- -rcp*gav*gas/g3a - arnv
    A2_3 	    <- -rcpgd*gvv*gvv/(gvv+ga) - rcp*gav*gav/g3a + rcpgd*gvv + rcp*gav - brnv
    # linking observed Tsurf with the source temperatures
    A3_1 	    <- 0
    A3_2 	    <- -aras - arav
    A3_3 	    <- -bras - brav
      # RHS
    B1 	      <- crns
    B2 	      <- crnv - rcpg*gvv*ga*da/(gvv+ga)
    B3 	      <- Mrad + cras + crav - ratm
    # SEB matrix solution [A|B] ; [X]=Inv[A][B]
    SEBvars   = SEBsoln(A1_1,A1_2,A1_3,A2_1,A2_2,A2_3,A3_1,A3_2,A3_3,B1,B2,B3)
    X1        <- SEBvars$X1;  X2  <- SEBvars$X2; X3  <- SEBvars$X3
    
    # output
    X0 	      <- (gas*X2 + gav*X3)/g3a
    d0 	      <- (rcpg*ga*da - X1 - rcpgd*gvv*X3)/(rcpg*(gvv + ga))
    LEs 	    <- X1
    LEv	      <- rcpg*gvv*(d0 + delta*X3)
    
    if (LEs < LEsmin){            
        # LHS
      A1_1    <- 0
      A1_2    <- -rcp*gas*gas/g3a - arns + rcp*gas
      A1_3    <- -rcp*gas*gav/g3a - brns
      A2_1    <- 1
      A2_2    <- -rcp*gav*gas/g3a - arnv
      A2_3    <- -rcp*gav*gav/g3a + rcp*gav - brnv
      # linking observed Tsurf with the source temperatures
      A3_1    <- 0
      A3_2    <- -aras - arav
      A3_3    <- -bras - brav
        # RHS
      B1 	    <- crns - LEsmin
      B2 	    <- crnv
      B3 	    <- Mrad + cras + crav - ratm
      
      # SEB matrix solution [A|B] ; [X]=Inv[A][B]
      # X1 = LEv; X2 = Ts-Ta; X3 = Tv-Ta;
      SEBvars = SEBsoln(A1_1,A1_2,A1_3,A2_1,A2_2,A2_3,A3_1,A3_2,A3_3,B1,B2,B3)
      X1      <- SEBvars$X1;  X2  <- SEBvars$X2; X3  <- SEBvars$X3
      
      # output
      X0      <- (gas*X2 + gav*X3)/g3a
      d0 	    <- da - (LEsmin + X1)/(rcpg*ga)
      LEv     <- X1;   LEs <- LEsmin
      
      if (LEv < LEvmin){
        # LHS
        A1_1 	<- -rcp*gas*gas/g3a - arns + rcp*gas
        A1_2 	<- -rcp*gas*gav/g3a - brns
        A2_1 	<- -rcp*gav*gas/g3a - arnv
        A2_2 	<- -rcp*gav*gav/g3a + rcp*gav - brnv
        # RHS
        B1 	  <- crns - LEsmin
        B2 	  <- crnv
        
        # SEB matrix solution [A|B] ; [X]=Inv[A][B]
        # X2 = Ts-Ta; X3 = Tv-Ta;
        detA 	<- A1_1*A2_2 - A1_2*A2_1
        X2 	  <- (1/detA)*(A2_2*B1 - A1_2*B2)
        X3 	  <- (1/detA)*(-A2_1*B1 + A1_1*B2)
        # output
        X0 	  <- (gas*X2 + gav*X3)/g3a
        d0 	  <- (ga*da - gss*delta*X2 - gvv*delta*X3)/g3
        LEv 	<- LEvmin; LEs <- LEsmin
      }
    }
    
    # convergence checks
    errSEB    <- abs(X0 - X0old);	Xold <- X0
    if (rg < 20){
      errSEB  <- 0.001
    }
    
    # end stability loop
  }
  
  # other SEB outputs - fluxes and temperatures
  rns 	      <- (crns + arns*X2 + brns*X3)/(1 - xg)
  rnv 	      <- (crnv + arnv*X2 + brnv*X3)
  rn 		      <- rns + rnv
  
  Hs 		      <- rcp*gas*(X2 - X0) 								# soil sensible heat
  Hv 		      <- rcp*gav*(X3 - X0) 								# vegetation sensible heat
  H 		      <- Hs + Hv 										      # overall sensible heat flux
  LE		      <- LEs + LEv										    # overall latent heat energy
  G 		      <- xg*rns
  
  T0 		      <- X0 + Ta 										      # aerodynamic temperature in [K]
  Ts 		      <- X2 + Ta 										      # soil temperature in [K]
  Tv 		      <- X3 + Ta 										      # vegetation temperature in [K]
  Tsf 	      <- ((emissf*ratm - cras - crav - X2*(aras + arav) - X3*(bras + brav))/(sigma*emissf))^0.25
  
  return (list(LE=LE,H=H,rn=rn,G=G,LEv=LEv,LEs=LEs,Hv=Hv,Hs=Hs,Tv=Tv,Ts=Ts,Tsf=Tsf))
}

calcRn        <- function(rg,ratm,emiss,emisv,albe,albv,fcov,fcovl,albsmn,albsmx,albmode){
# calculate rn forcing terms
  if (albmode != 'Capped'){
    albs      <- (albe - fcov*albv)/((1 - fcov)**2 + fcov*albv*albe - (fcov*albv)^2)
  } else{
    albs 	    <- max(albsmn,min(albsmx,(albe - fcov*albv)/((1 - fcov)**2 + fcov*albv*albe - (fcov*albv)^2)))		
  } 
  # albs 	    <- (albe - fcov*albv)/((1 - fcov)**2 + fcov*albv*albe - (fcov*albv)**2)
  # albs 	    <- max(albsmn,min(albsmn,(albe - fcov*albv)/((1 - fcov)**2 + fcov*albv*albe - (fcov*albv)**2)))
  v1          <- 1 - albv*albs*fcov; 	v1a = 1 - albv*albs*fcovl
  v2 	        <- 1 - emisv
  v3 	        <- 1 - emiss
  v4 		      <- 1 - fcov;          v4a <- 1 - fcovl
  v5 		      <- 1 - fcov*v2*v3; 		v5a <- 1 - fcovl*v2*v3
  arns 	      <- -(v4a*emiss + emisv*emiss*fcovl)/v5a
  brns 	      <- (emisv*emiss*fcovl)/v5a
  crns 	      <- (rg*(1 - albs)*v4)/v1 + (v4a*emiss*ratm)/v5a
  cras 	      <- (v4a*emiss*ratm)/v5a
  arnv 	      <- brns
  brnv 	      <- -fcovl*(emisv + (emisv*emiss + v4a*v3*emisv)/v5a)
  crnv 	      <- rg*(1 - albv)*fcov*(1 + (albs*v4)/v1) + fcovl*emisv*ratm*(1 + (v4a*v3)/v5a)
  crav 	      <- fcovl*emisv*ratm*(1 + (v4a*v3)/v5a)
  
  return (list(albs=albs,arns=arns,brns=brns,crns=crns,arnv=arnv,brnv=brnv,crnv=crnv,cras=cras,crav=crav))
}

SEBsoln       <- function(A1_1,A1_2,A1_3,A2_1,A2_2,A2_3,A3_1,A3_2,A3_3,B1,B2,B3){
# SEB matrix solution [A|B] ; [X]=Inv[A][B]
  # determinant of A
  detA 	      <- A1_1*(A2_2*A3_3 - A2_3*A3_2) - A1_2*(A2_1*A3_3 - A2_3*A3_1) + A1_3*(A2_1*A3_2 - A2_2*A3_1)
  # inverse matrix coefficients
  IA1_1	      <-  (A2_2*A3_3 - A2_3*A3_2)/detA
  IA1_2	      <- -(A1_2*A3_3 - A1_3*A3_2)/detA
  IA1_3	      <-  (A1_2*A2_3 - A1_3*A2_2)/detA
  IA2_1	      <- -(A2_1*A3_3 - A2_3*A3_1)/detA
  IA2_2	      <-  (A1_1*A3_3 - A1_3*A3_1)/detA
  IA2_3	      <- -(A1_1*A2_3 - A1_3*A2_1)/detA
  IA3_1	      <-  (A2_1*A3_2 - A2_2*A3_1)/detA
  IA3_2	      <- -(A1_1*A3_2 - A1_2*A3_1)/detA
  IA3_3	      <-  (A1_1*A2_2 - A1_2*A2_1)/detA
  # solution
  X1 	        <- IA1_1*B1 + IA1_2*B2 + IA1_3*B3                                                    # LEs or LEv
  X2 	        <- IA2_1*B1 + IA2_2*B2 + IA2_3*B3                                                    # Ts-Ta
  X3 	        <- IA3_1*B1 + IA3_2*B2 + IA3_3*B3                                                    # Tv-Ta
  
  return (list(X1=X1,X2=X2,X3=X3))
}

#--uΓu--

#======================================================================================================================================
### test - see https://runningfingers.com/seb.php
#

Tsurf           <- 297.24
vza             <- 0
rg              <- 630
Ta              <- 293.15
rh              <- 50
ua              <- 2
za              <- 3
lai             <- 1.5; glai <- 1.5
zf              <- 1
rstmin          <- 100
albv            <- 0.18
emisv           <- 0.98; emiss <- 0.96; emissf <- 0.97
albe            <- 0.3
xg              <- 0.315
sigmoy          <- 0.5
albmode         <- 'UnCapped'

# call SPARSE
OutputVars       = SPARSE(Tsurf,vza,rg,Ta,rh,ua,za,lai,glai,zf,rstmin,albv,emisv,emiss,emissf,albe,xg,sigmoy,albmode)

LE              <- OutputVars$LE;   H               <- OutputVars$H
rn              <- OutputVars$rn;   G               <- OutputVars$G
LEv             <- OutputVars$LEv;  LEs             <- OutputVars$LEs; Hv               <- OutputVars$Hv;  Hs              <- OutputVars$Hs
Tv              <- OutputVars$Tv;   Ts              <- OutputVars$Ts;  Tsf              <- OutputVars$Tsf

###
