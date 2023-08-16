/* Historical stock data - NSE
-- ufu --
*/

runchart();

// retrieve stock data (price, volume, ...)

function runchart(){
//var date = [<?php echo $dat1; ?>];
//var price = [<?php echo $dat2; ?>];
//var price = [<?php echo json_encode($dat2); ?>];

    var sfx = document.getElementById("sfx").value.toUpperCase();
    var per = document.getElementById("per").value;
    
    // display ABSA's chart initially
    if (sfx.length == 0){
        var sfx = 'ABSA';
    }
    
    var xmlhttp = new XMLHttpRequest();
    /*xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        document.getElementById("txtHint").innerHTML = this.responseText;
      }
    };*/
    ///price
    xmlhttp.open("GET","php/price.php?q="+sfx+"&p="+per,true);
    xmlhttp.send();
    xmlhttp.onload = function() {
        var price = this.response;
        var price0 = "'"+JSON.parse("["+price+"]")+"'";
        var price = price0.split(',').map(Number);
        //var price = price0.split(",");
        //alert(price);
        
        ///volume
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET","php/vol.php?q="+sfx+"&p="+per,true);
        xmlhttp.send();
        xmlhttp.onload = function() {
            var vol = this.response;
            var vol0 = "'"+JSON.parse("["+vol+"]")+"'";
            var vol = vol0.split(',').map(Number);
        
            ///date
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("GET","php/date.php?q="+sfx+"&p="+per,true);
            xmlhttp.send();
            xmlhttp.onload = function() {
                var date = this.response;
                var date = JSON.parse(date);
                //alert(date.length);
                /*var date = new Array(price.length);
                for (i=0;i<price.length;i++){
                    date[i] = i+1;
                }*/
            
            // plotting
            
            if (per < 50) {
                var volcol = "rgb(205, 205, 205)";
            } else {
                if (per > 365){
                    var volcol = "rgb(0,0,0)";
                } else {
                    var volcol = "rgb(150, 150, 150)";
                }
            }

            var ctx = document.getElementById('sec_fx').getContext('2d');
            
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
                labels: date,
                datasets: [{
                    label: sfx+" (KES)",
                    backgroundColor: 'rgba(255, 255, 255,0)',
                    borderColor: 'rgb(0, 0, 255)',
                    data: price,
        			pointRadius: 0.5,
        			pointStyle: 'line',
        			borderWidth: 1,
        			yAxisID: 'P'
                },{
                    label: 'volume',
                    backgroundColor: volcol,
                    borderColor: 'rgb(125, 125, 125)',
                    data: vol,
        			pointRadius: 1,
        			pointStyle: 'line',
        			borderWidth: 1,
        			type : 'bar',
        			yAxisID: 'V'
                }/*,{
                    label: 'Analysis/update',
                    backgroundColor: 'rgba(255, 255, 255,0)',
                    borderColor: 'rgb(0, 255, 0)',
                    data: [<?php echo $dat1; ?>],
        			pointRadius: 0.5,
        			borderWidth: 1
                },{
                    label: 'Openloop init. w/ update',
                    backgroundColor: 'rgba(255, 255, 255,0)',
                    borderColor: 'rgb(0, 0, 255)',
                    data: X_ol,
        			pointRadius: 0.5,
        			borderWidth: 1
                },{
                    label: 'Openloop w/ prior init',
                    backgroundColor: 'rgba(255, 255, 255,0)',
                    borderColor: 'rgb(255, 0, 255)',
                    data: X_ol_Prior_init,
        			pointRadius: 0.5,
        			borderWidth: 1
                }*/]
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
                labelString: 'Date [yyyy-mm-dd]',
                fontColor: '#000',
        		fontSize: '12'
              },
              ticks: {
                fontSize: 14,
                fontColor: '#000',
                autoSkip: true,
                maxTicksLimit: 5,
                maxRotation: 0,
                minRotation: 0
              }
            }],
            yAxes: [{
              id: 'P',
              //type: 'linear',
              position: 'left',
        	  gridLines: {
                display: true,
        		drawOnChartArea: false
              },
              scaleLabel: {
                display: true,
                labelString: 'Price (KES)',
                fontColor: '#000',
        		fontSize: '12'
              },
              ticks: {
                fontSize: 12,
                fontColor: '#000',
                autoSkip: true,
                maxTicksLimit: 5
              }
            },{
              id: 'V',
              //type: 'linear',
              position: 'right',
              /*ticks: {
                max: 1,
                min: 0
              },*/
              gridLines: {
                display: true,
        		drawOnChartArea: false
              },
              scaleLabel: {
                display: true,
                labelString: 'Volume',
                fontColor: '#000',
        		fontSize: '12'
              },
              ticks: {
                fontSize: 12,
                fontColor: '#000',
                autoSkip: true,
                maxTicksLimit: 5
              }
            }]
          },
          legend: {
            display: true,
              labels: {
                    filter: function(legendItem, chartData) {
                        if (legendItem.datasetIndex === 1) {
                          return false;
                        }
                       return true;
                    },
                    //fontColor: 'rgb(0,0,0)',
                    //boxWidth: 10,
                    //padding: 5,
                    fontSize:16,
                    fontColor: '#000',
                    usePointStyle: true
                  }
                }
        	}
        });
        //
        }
      }  
        
    }

}

//Stock ticker symbols : Nairobi Securities Exchange

function showHint(str) {
  if (str.length == 0) {
    document.getElementById("txtHint").innerHTML = "";
    return;
  } else {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var xxx0 = this.responseText;
        var xxx = xxx0.replace(/\s+/g, '');
        xxx = xxx.split(",");
        var xxxstr = '';
        
        for (i=0;i<xxx.length;i++){
            var xx = "getsfx('"+xxx[i]+"')";
            xxxstr = xxxstr + "<button type='button' class='ddg_search' onclick="+xx+">"+xxx[i]+"</button>";
        }
        
        if (this.responseText.replace(/\s+/g, '') === "securitynotfound‼"){
            document.getElementById("txtHint").innerHTML = this.responseText;
        } else {
            document.getElementById("txtHint").innerHTML = xxxstr;
        }
        //document.getElementById("txtHint").innerHTML = this.responseText;
      }
    };
    xmlhttp.open("GET", "php/symbols.php?q=" + str, true);
    xmlhttp.send();
  }
}
function getsfx(x){
    x = x.replace(/\s+/g, '');
    //alert(typeof(x));
    document.getElementById("sfx").value=x;
}