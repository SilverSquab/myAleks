

//查看报告
$('.tdOnReport .text').on('click',function (){
    var name = $(this).attr("name");
    var url = 'http://47.110.253.251/templates-static/templates/'+name+'.html'
    window.open(url);
});

//下载pdf文档
$('.tdOnDownload .text').on('click',function (){
    var url=$(this).attr("name");
    var url = 'http://47.110.253.251/templates-static/'+name+'.pdf';
    window.open(url);
});




//选择班级
$('.classCheckLi div').on('click',function(){
    //获取班级id
    var classId = $(this).attr("name");
     //存储选择，改变显示
    $("#classInput").val($(this).text());
    $.session.set("classId",classId);
    $.session.remove('studentId');
    $("#studentInput").val('');
    //发送班级id获取该班学生列表
    $.ajax({
      type:'POST',
      url: "http://127.0.01:5000/LearningInformation/getStudentList",
      dataType:'json',
      contentType:'application/json;charset=UTF-8',
      data: JSON.stringify({"classId":classId}),
      success:function(data,status){
      console.info(data)
        //alert("成功")
        console.info($.session.get("classId"))
     },error:function () {
           alert('提交失败！')
     }
    })
});

//学生框联动获取数据
$('.studentCheckLi div').on('click',function(){
     var studentId = $(this).attr("name");
    $.session.set("studentId",studentId);
    $("#studentInput").val($(this).text());
});

//查询方法
$('#checkButton .text').on('click',function(){
    //曲线图数据容器
    var lineValue;
    //获取下拉框选择
    var studentId = $.session.get("studentId");
    var classId = $.session.get("classId")
   //发送请求，获取报表的数据
    $.ajax({
      type:'POST',
      url: "http://127.0.01:5000/LearningInformation/getLearningInformation",
      dataType:'json',
      contentType:'application/json;charset=UTF-8',
      data: JSON.stringify({"classId":classId,"studentId":studentId}),
      success:function(data,status){
        lineValue = data.lineValue;
        alert("成功");
     },error:function () {
        alert('提交失败！')
     }
    })


    //若数据为空则不画曲线图
//    if(!lineValue){
//       console.info("数据为空，不画表");
//       return ;
//    }

   // 画图
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
//    labels: ["2019-08-1", "2019-08-2", "2019-08-3", "2019-08-4", "2019-08-5", "2019-08-6", "2019-08-7", "2019-08-8"],
    labels:lineValue.labels,
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
//      data: [20, 30, 40, 30, 50, 60, 30, 50],
       data:lineValue.data,
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


})











