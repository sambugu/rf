/*
Chaos Theory : Lorenz Butterfly algorithm - Lorenz (1963) : https://doi.org/10.1175/1520-0469(1963)020%3C0130:DNF%3E2.0.CO;2
The deterministic non-periodic flow algorithm as presented in Lorenz (1963)
	one-step integration of the numerical solution of a simple system
	representing cellular convection :
            Inputs : initial state ; parameters - rho, sigma, beta ; timestep 
	
        .This is free software under the GNU General Public License v3.0.
        .GNU Licence : https://www.gnu.org/licenses/gpl-3.0-standalone.html

	. translated from Lisa.Neef.13 matlab code : https://github.com/LisaNeef/Data-Assimilation-Practicals-Matlab/blob/master/lorenz63.m
-- ufu -- JS from 250823
*/

function run_lorenz63(){
	
	var T					= document.getElementById("timesteps").value - 0; //or *1
	var sigma				= document.getElementById("sigma").value - 0; //or *1
	var rho					= document.getElementById("rho").value - 0; //or *1
	var beta				= document.getElementById("beta").value - 0; //or *1
	var dt					= document.getElementById("time_step").value - 0; //or *1
	var xin					= document.getElementById("Xinit").value - 0; //or *1
	var yin					= document.getElementById("Yinit").value - 0; //or *1
	var zin					= document.getElementById("Zinit").value - 0; //or *1
	
	var X					= new Array(T);
	var Y					= new Array(T);
	var Z					= new Array(T);
	var X_Z                 = [{x:xin,y:zin}];
	//var X_Z                 = {x:xin,y:zin};
	
	//xin						= xin*randn_bm();
	//yin						= yin*randn_bm();
	//zin						= zin*randn_bm();
	
	for (i=0;i<T;i++){
		[xout,yout,zout]	= lorenz(xin,yin,zin,sigma,rho,beta,dt);
		X[i]				= xout; Y[i] = yout; Z[i] = zout;
		//X_Z.push({x:xout,y:zout});
		X_Z[i]              = {x:xout,y:zout};
		xin					= xout; yin = yout; zin = zout;
	}
	
// plotting

var ctx = document.getElementById('butterfly').getContext('2d');

//
if(window.bar != undefined){
    window.bar.destroy();
}
window.bar = new Chart(ctx, {
//

//var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'scatter',
    data: {
        //labels: X,
        datasets: [{
            label: 'X-Z 2D SPACE',
            backgroundColor: 'rgba(255, 255, 255,0)',
            borderColor: 'rgb(125, 0, 125)',
            data: X_Z
			//pointRadius: 1,
			//pointStyle: 'line',
			//borderWidth: 1
        }]
    },

    // Configuration options go here
    options: {
		scales: {
	xAxes: [{
	  gridLines: {
        display: false,
		drawOnChartArea: false
      },
      scaleLabel: {
        display: true,
        labelString: 'state (X)',
		fontSize: '16'
      },
      ticks: {
        fontSize: 12,
        autoSkip: true,
        maxTicksLimit: 20,
        maxRotation: 0,
        minRotation: 0
      }
    }],
    yAxes: [{
	  gridLines: {
        display: true,
		drawOnChartArea: false
      },
      scaleLabel: {
        display: true,
        labelString: 'state (Z)',
		fontSize: '16'
      }
    }]
  },
  legend: {
    display: true,
      labels: {
            //fontColor: 'rgb(0,0,0)',
            //boxWidth: 10,
            //padding: 5,
            //fontSize:16,
            //fontColor: '#000',
            usePointStyle: true
          }
        }
	}
});
//

    }
    
    function lorenz(xin,yin,zin,sigma,rho,beta,dt){
	
    // Integration of xin using the numerical solution of the Lorenz model
        // Mean trajectory calculation
    const w1				= 1/6; const w2 = 1/3; const w3 = 1/3; const w4 = 1/6;

    let xin1				= xin; let yin1 = yin; let zin1 = zin;
    [fpx,fpy,fpz]			= lorenzRHS(xin1,yin1,zin1,sigma,rho,beta);
    let x1					= dt*fpx; let y1 = dt*fpy; let z1 = dt*fpz;

    let xin2				= xin + 0.5*x1; let yin2 = yin + 0.5*y1; let zin2 = zin + 0.5*z1;
    [fpx,fpy,fpz]			= lorenzRHS(xin2,yin2,zin2,sigma,rho,beta);
    let x2					= dt*fpx; let y2 = dt*fpy; let z2 = dt*fpz;

    let xin3				= xin + 0.5*x2; let yin3 = yin + 0.5*y2; let zin3 = zin + 0.5*z2;
    [fpx,fpy,fpz]			= lorenzRHS(xin3,yin3,zin3,sigma,rho,beta);
    let x3					= dt*fpx; let y3 = dt*fpy; let z3 = dt*fpz;

    // x4 = Xin + x3                                                                                                     ### corrected from xx4 = xin+ x3; in lisaneef's .m script-- commented out : throws overflow errors ...nans in both .py and .m

    // ADDED : correction for var x4 --- overflow errors disparu
    let xin4				= xin + 0.5*x3; let yin4 = yin + 0.5*y3; let zin4 = zin + 0.5*z3;
    [fpx,fpy,fpz]			= lorenzRHS(xin4,yin4,zin4,sigma,rho,beta);
    let x4					= dt*fpx; let y4 = dt*fpy; let z4 = dt*fpz;

    let xout				= xin + w1*x1 + w2*x2 + w3*x3 + w4*x4;
	let yout				= yin + w1*y1 + w2*y2 + w3*y3 + w4*y4;
	let zout				= zin + w1*z1 + w2*z2 + w3*z3 + w4*z4;

    return [xout,yout,zout];
}

function lorenzRHS(x,y,z,sigma,rho,beta){
	
	// RHS of eqs. (25)-(27) of Lorenz (1963) ; also see Lorenz (1986) p1550
	fpx						= sigma*(y - x);
	fpy						= rho*x - y - x*z;
	fpz						= x*y - beta*z;                                

	return [fpx,fpy,fpz];
}
    
// Standard Normal variate using Box-Muller transform.
function randn_bm() {
    var u = 0, v = 0;
    while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
    while(v === 0) v = Math.random();
    return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
}

//--uΓu--    
    
