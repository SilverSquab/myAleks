(function () {
    $.MsgBox = {
        Confirm: function (planInfo,callback) {
            GenerateHtml(planInfo);
            btnNo();
            buy(callback);
        }
    }
    //生成Html
    var GenerateHtml = function (planInfo) {
        var _html = "";
        _html += '<div id="mb_box"></div>'
                +'<div id="mb_con1" style="padding-top:20px;height: 80%"><span id="mb_tit" fontSize="30px"><i fas fa-search>套餐信息</i></span><a id="mb_ico">X</a>'
                +'<div class="row" id="question-container"  style=" width:99.5%;height:90%;overflow-y: scroll">';
        for (var index in planInfo){
             _html += '<div class="col-lg-6">'
                          +' <div class="card mb-4" name="Cls">'
                              +' <div class="card-header">'
                                  +' <div class="custom-control custom-checkbox small" style="float: left">'
                                      +' <h6 class="m-0 font-weight-bold text-primary"'
                                                                       +' style="line-height: 1.5rem;">套餐名称：'+planInfo[index].name+'</h6>'
                                  +' </div>'
                                  +' <div style="float: right">'
                                      +' <button class="btn btn-primary" id='+'"'+planInfo[index].id+'"'+ 'name="buyPlan" type="button">'
                                          +' <i>选择套餐</i>'
                                      +' </button>'
                                  +' </div>'
                              +' </div>'
                              +' <div class="card-body">'
                                  +' <p>套餐信息：'+planInfo[index].info+'</p>'
                                  +' <p>描述：'+planInfo[index].description+'</p>'
                                  +' <p>价格：'+planInfo[index].default_price+'</p>'
                                  +' <p>对应科目：'+planInfo[index].subject+'</p>'
                                  +' <p>资源：';
                                  var resources = $.parseJSON(planInfo[index].resources)
                                  //console.log(resources)
                                  for (var key in resources){
                                     _html+=key+"("+resources[key]+"次)、"
                                  }
                                  _html+= '</p>'
                              +' </div>'
                          +' </div>'
                    +' </div>'
        }
        _html += '</div></div>'
        //必须先将_html添加到body，再设置Css样式
        $("body").append(_html); 
        //生成Css
         GenerateCss();
    }
 
    //生成Css
    var GenerateCss = function () {
        $("#mb_box").css({ width: '100%', height: '100%', zIndex: '99999', position: 'fixed',
            filter: 'Alpha(opacity=60)', backgroundColor: 'black', top: '0', left: '0', opacity: '0.6'
        });
        $("#mb_con1").css({ zIndex: '999999', width: '80%', position: 'fixed',//弹框的宽
            backgroundColor: 'White', borderRadius: '15px'
        });
        $("#mb_tit").css({ display: 'block', fontSize: '20px', color: '#009688', padding: '10px 15px',//字体颜色
            backgroundColor: 'white', borderRadius: '15px 15px 0 0',//顶部title颜色
            borderBottom: '3px solid #009688', fontWeight: 'bold'//线条颜色
        });
        $("#mb_msg").css({ padding: '20px', lineHeight: '20px',
            borderBottom: '1px dashed #DDD', fontSize: '13px'//虚线分界线颜色
        });
        $("#mb_ico").css({ display: 'block', position: 'absolute', right: '10px', top: '9px',
            border: '1px solid #009688', width: '18px', height: '18px', textAlign: 'center',//关闭图标外圈颜色
            lineHeight: '16px', cursor: 'pointer', borderRadius: '12px', fontFamily: '微软雅黑'
        });
        $("#mb_btnbox").css({ margin: '15px 0 10px 0', textAlign: 'center' });
        $("#mb_btn_ok,#mb_btn_no").css({ width: '85px', height: '30px', color: 'white', border: 'none' });
        $("#mb_btn_ok").css({ backgroundColor: '#1fc88d' });//按钮颜色
        $("#mb_btn_no").css({ backgroundColor: '#1fc88d', marginLeft: '20px' });//按钮颜色
        //右上角关闭按钮hover样式
        $("#mb_ico").hover(function () {
            $(this).css({ backgroundColor: '#009688', color: 'White' });//鼠标悬停效果
        }, function () {
            $(this).css({ backgroundColor: 'White', color: '#009688' });//鼠标离开之后效果
        });
        var _widht = document.documentElement.clientWidth;  //屏幕宽
        var _height = document.documentElement.clientHeight; //屏幕高
        var boxWidth = $("#mb_con1").width();
        var boxHeight = $("#mb_con1").height();
		console.log(_widht)
		console.log(document.body.clientHeight)
		console.log(boxWidth)
		console.log(boxHeight)
        //让提示框居中
        $("#mb_con1").css({ top: (_height - boxHeight) / 2 + "px", left: (_widht - boxWidth) / 2 + "px" });
    }
    //取消按钮事件
    var btnNo = function () {
        $("#mb_btn_no,#mb_ico").click(function () {
            $("#mb_box,#mb_con1").remove();
        });
    }
    //购买套餐事件
    var buy = function (callback) {
        callback();
    }
})();
