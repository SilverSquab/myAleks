// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}



//选择班级
$('.classCheckLi div').on('click',function(){
    //获取班级id
    var classId = $(this).attr("name");
    //存储选择，改变显示
    $("#classInput").val($(this).text());
    $.session.set("classId",classId);
});

//学生查询方法
$('.tdOnStudent .text').on('click',function(){
     var studentId = $(this).attr("name");
     var classId = $.session.get("classId");
    $.session.set("studentId",studentId);
    //发送请求，获取报表的数据
    $(location).attr('href',"http://47.110.253.251/abc/teacher/index/?classId="+classId+"&studentId="+studentId);

});

//班级查询方法
$('#checkButton .text').on('click',function(){
    //获取选择
    var classId = $.session.get("classId");
    $.session.remove('studentId');
   //发送请求，获取报表的数据
    $(location).attr('href',"http://47.110.253.251/abc/teacher/index/?classId="+classId);
})

//学生获取成绩数据
var getStudentDrawData = function (classId,studentId) {
    //发送请求获取成绩
    $.ajax({
        type:'POST',
        url: "http://47.110.253.251/abc/teacher/ajax-get-scores-student/",
        dataType:'json',
        contentType:'application/json;charset=UTF-8',
        data: JSON.stringify({"classId":classId,"studentId":studentId}),
        success:function(data,status){
            //调用画图方法
            if(data){
                drawGraphs(data.time,data.score);
            }else{
                drawGraphs([],[]);
            }
        },error:function () {
        }
    })
}
//班级获取成绩数据
var getClassDrawData = function (classId) {
    //发送请求获取成绩
    $.ajax({
        type:'POST',
        url: "http://47.110.253.251/abc/teacher/ajax-get-scores-class/",
        dataType:'json',
        contentType:'application/json;charset=UTF-8',
        data: JSON.stringify({"classId":classId}),
        success:function(data,status){
            //调用画图方法
            if(data){
                drawGraphs(data.time,data.score);
            }else{
                drawGraphs([],[]);
            }
        },error:function () {
        }
    })
}




// 画图
var drawGraphs = function(labels,data){
    var ctx = document.getElementById("myAreaChart");
    var myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels:labels,
        datasets: [{
          label: "成绩",
          lineTension: 0.3,
          backgroundColor: "rgba(78, 115, 223, 0.05)",
          borderColor: "rgba(78, 115, 223, 1)",
          pointRadius: 3,
          pointBackgroundColor: "rgba(78, 115, 223, 1)",
          pointBorderColor: "rgba(78, 115, 223, 1)",
          pointHoverRadius: 3,
          pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
          pointHoverBorderColor: "rgba(78, 115, 223, 1)",
          pointHitRadius: 10,
          pointBorderWidth: 2,
           data:data,
        }],
      },
      options: {
        maintainAspectRatio: false,
        layout: {
          padding: {
            left: 10,
            right: 25,
            top: 25,
            bottom: 0
          }
        },
        scales: {
          xAxes: [{
            time: {
              unit: 'date'
            },
            gridLines: {
              display: false,
              drawBorder: false
            },
            ticks: {
              maxTicksLimit: 7
            }
          }],
          yAxes: [{
            ticks: {
              maxTicksLimit: 5,
              padding: 10,
              // Include a dollar sign in the ticks
              callback: function(value, index, values) {
                return  number_format(value);
              }
            },
            gridLines: {
              color: "rgb(234, 236, 244)",
              zeroLineColor: "rgb(234, 236, 244)",
              drawBorder: false,
              borderDash: [2],
              zeroLineBorderDash: [2]
            }
          }],
        },
        legend: {
          display: false
        },
        tooltips: {
          backgroundColor: "rgb(255,255,255)",
          bodyFontColor: "#858796",
          titleMarginBottom: 10,
          titleFontColor: '#6e707e',
          titleFontSize: 14,
          borderColor: '#dddfeb',
          borderWidth: 1,
          xPadding: 15,
          yPadding: 15,
          displayColors: false,
          intersect: false,
          mode: 'index',
          caretPadding: 10,
          callbacks: {
            label: function(tooltipItem, chart) {
              var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
              return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
            }
          }
        }
      }
    });
}

//查看报告
//$(document).on('click','.tdOnReport .text',function(){
//   var name = $(this).attr("name");
//    var url = 'http://47.110.253.251/templates-static/templates/html/'+name+'.html'
//    window.open(url);
//})
//下载pdf文档
//$(document).on('click','.tdOnDownload .text',function(){
//    var name = $(this).attr("name");
//    var url = 'http://47.110.253.251/templates-static/templates/pdf/'+name+'.pdf'
//    window.open(url);
//})









