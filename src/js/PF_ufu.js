
/* Particle filtering algorithm - Gordon and Salmond (1993) - JavaScript implementation
-- ufu -- JS from 220220
*/
	
function runPF(){
var Np 				= document.getElementById("particles").value - 0;
var T 				= document.getElementById("timesteps").value - 0; //or *1
//document.getElementById("demo").innerHTML = Np;
var Xinit 			= document.getElementById("init").value*1;
var sd 				= document.getElementById("pert").value*1; //or - 0
//var sd = 1; // hardcoded for convenience
var initXvar 		= 2; // hardcoded for convenience
var pdf 			= document.getElementById("pdf").value;
var X_lklhd 		= new Array(T); //empty array to hold the likelihood/observations
var X_analysis 		= new Array(T); //empty array to hold the updates/posteriors
var X_ol 			= new Array(T); //empty array to hold the open-loop estimates - initialized with previous timestep's posterior
var X_ol_Prior_init = new Array(T); //empty array to hold the open-loop estimates - initialized with previous timestep's prior
var Xensemble 		= new Array(Np); //empty array to hold the particles
var Xaxis 			= new Array(T);


// create initial backgrounds/priors by perturbing Xinit
for (i=0;i<Np;i++){
	if (pdf != 'Normal'){
		var rand 	= (2*Math.random() - 1)*Math.PI;
		} else {
		var rand 	= randn_bm();
		}
Xensemble[i] 		= Xinit + Math.sqrt(initXvar)*rand;
}
	// initial prior mean
	var Xinit_Pr 	= getAverage(Xensemble,Np);


for (t=0;t<T;t++){

// integrate model forward for the observation 'truth'
	if (pdf != 'Normal'){
		var rand 	= (2*Math.random() - 1)*Math.PI;
		} else {
		var rand 	= randn_bm();
		}
var X 				= 0.5*Xinit + 25*Xinit/(1 + Math.pow(Xinit,2)) + 8*Math.cos(1.2*(t - 1)) + Math.sqrt(sd)*rand;
// the observation to be assimilated i.e. X through the observation model : Y = h(X)
	if (pdf != 'Normal'){
		var rand 	= (2*Math.random() - 1)*Math.PI;
		} else {
		var rand 	= randn_bm();
		}
var Y = Math.pow(X,2)/20 + Math.sqrt(sd)*rand;

	var wts 		= new Array(Np); //empty array to hold the particle weights
	var Xprior 		= new Array(Np); // ensemble array to hold the backgrounds/priors
	var Yprior 		= new Array(Np); // ensemble to hold the mapped observations, h(x)
	//var Xupdate = new Array(Np); // empty array to hold the posterior/analyses
	
	for (i=0;i<Np;i++){
	
		var Xinit_i = Xensemble[i];
		
		// integrate particle i through the process model
			if (pdf != 'Normal'){
				var rand = (2*Math.random() - 1)*Math.PI;
			} else {
				var rand = randn_bm();
			}
		Xprior[i] 	= 0.5*Xinit_i + 25*Xinit_i/(1 + Math.pow(Xinit_i,2)) + 8*Math.cos(1.2*(t - 1)) + Math.sqrt(sd)*rand; // process model : f(Xinit_i)
		Yprior[i] 	= Math.pow(Xprior[i],2)/20;
		
		// particle weights calculation
		var wt 		= 1/Math.sqrt(2*Math.PI*Math.pow(sd,2))*Math.pow(Math.E,(-(Math.pow((Y-Yprior[i]),2))/(2*Math.pow(sd,2))));
		wts[i] 		= wt;	
	}
	// normalize the weights | for sum(wts)=1
	var wts2 		= wts;
	var sm 			= 0;
	
	for (i=0;i<Np;i++){
		sm += wts[i];
	}
	
	for (i=0;i<Np;i++){
		wts[i] 		= wts2[i]/sm;
	}
	
	// open-loop estimate : initialized using update/posterior from previous timestep
	X_ol[t] 		= getAverage(Xprior,Np);
	// open-loop estimate : initialized using prior from previous timestep
	X_ol_Prior_init[t] = 0.5*Xinit_Pr + 25*Xinit_Pr/(1 + Math.pow(Xinit_Pr,2)) + 8*Math.cos(1.2*(t - 1)); // process model : f(Xinit_Pr)
	Xinit_Pr 		= X_ol_Prior_init[t] // as initial condition for the next timestep
	// resampling
	var Xupdatens 	= SIR(wts,Xprior,Np);
	// best estimate/analysis
	X_analysis[t] 	= getAverage(Xupdatens,Np);
	
	Xensemble 		= Xupdatens;
X_lklhd[t] 			= X;	
Xinit 				= X;

Xaxis[t] 			= t+1;
}

/*
document.getElementById("demo").innerHTML = X_analysis;
document.getElementById("demo1").innerHTML = X_lklhd;
document.getElementById("demo2").innerHTML = X_ol;
document.getElementById("demo3").innerHTML = X_ol_Prior_init;
*/

// plotting

var ctx = document.getElementById('PFseries').getContext('2d');

//
if(window.bar != undefined){
    window.bar.destroy();
}
window.bar = new Chart(ctx, {
//

//var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: Xaxis,
        datasets: [{
            label: 'Likelihood',
            backgroundColor: 'rgba(255, 255, 255,0)',
            borderColor: 'rgb(0, 0, 0)',
            data: X_lklhd,
			pointRadius: 0.5,
			pointStyle: 'line',
			borderWidth: 1
        },{
            label: 'Analysis/update',
            backgroundColor: 'rgba(255, 255, 255,0)',
            borderColor: 'rgb(0, 255, 0)',
            data: X_analysis,
			pointRadius: 0.5,
			pointStyle: 'line',
			borderWidth: 1
        },{
            label: 'Openloop init. w/ update',
            backgroundColor: 'rgba(255, 255, 255,0)',
            borderColor: 'rgb(0, 0, 255)',
            data: X_ol,
			pointRadius: 0.5,
			pointStyle: 'line',
			borderWidth: 1
        },{
            label: 'Openloop w/ prior init',
            backgroundColor: 'rgba(255, 255, 255,0)',
            borderColor: 'rgb(255, 0, 255)',
            data: X_ol_Prior_init,
			pointRadius: 0.5,
			pointStyle: 'line',
			borderWidth: 1
        }]
    },

    // Configuration options go here
    options: {
		scales: {
	xAxes: [{
	  gridLines: {
        display: true,
		drawOnChartArea: false
      },
      scaleLabel: {
        display: true,
        labelString: 'time (t)',
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
        labelString: 'state (X)',
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

function SIR(wts,Xprior,Np){
	var Xupdate 		= new Array(Np);
	// sequential importance resampling
	var cumsum 			= new Array(Np);
	cumsum[0] 			= wts[0];
	for (j=1;j<Np;j++){
		cumsum[j] 		= cumsum[j-1] + wts[j];
	}
	for (i=0;i<Np;i++){
		var rnd_sample 	= Math.random();
		var satCrit 	= cumsum.find(resample);
		var ind 		= cumsum.indexOf(satCrit);
		Xupdate[i] 		= Xprior[ind];
	}
	return Xupdate

	function resample(value, index, array){
	//var indval = rnd_sample <= value;
	  return rnd_sample <= value;
	}
}

function getAverage(ensemble,N){
	var sum 			= 0;
	for (i=0;i<N;i++){
		sum += ensemble[i]; 
	}
	return sum/N;
}

// Standard Normal variate using Box-Muller transform.
function randn_bm() {
    var u = 0, v = 0;
    while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
    while(v === 0) v = Math.random();
    return Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
}

//--uΓu--
