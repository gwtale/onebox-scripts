$(document).ready(function() {
    $("#main_form").fadeIn(800)
    $(".span3").hide()
    $(".span9").attr("class","")    
    $("#add_cash").click(function(){
        $.getJSON("/userinfo/push_cash_modify",  
                  {user_id:$("#user_id").val(),money:$("#money").val(),days:$("#days").val()
                  },  
                   function(data){
                    if(data.status=='ok'){
                        $("#cash_form").fadeOut(400)
                        $("#cash_ok").fadeIn(900)
                        $("#cash_ok").html("充值成功<br>到期时间:"+data.expire_date+"<br><a href='/userinfo/user_list'><span class='label label-success' >点击返回</span></a>")
                        
                    }else{
                        $("#cash_form").fadeOut(400)
                        $("#cash_error").fadeIn(900)
                    }                
        }); 
    });
});

