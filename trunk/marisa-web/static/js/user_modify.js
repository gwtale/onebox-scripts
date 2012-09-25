$(document).ready(function() {
    if($("#user_id").val()=="None"){
        $("#user_id").val('')
    }else{
         $.getJSON("/userinfo/get_user_info",  
                  {user_id:$("#user_id").val()
                  },  
                   function(data){
                    if(data.status=='ok'){
                        $("#user_id_parent").attr('class','control-group success')
                        $("#client_type").val(data.user.client_type)
                        $("#submit_modify_user").removeAttr('disabled')
                        $("#username").val(data.user.username)
                        $("#password").val(data.user.password)
                        $("#user_state").html(data.user.user_state)
                        $("#expire_date_rd").val(data.user.expire_date)
                        $("#expire_date_rd").attr('data-date',data.user.expire_date)
                        $("#last_login").val(data.user.last_login)
            
                    }else{
                     $("#submit_modify_user").attr('disabled',"disabled")
                        $("#user_id_parent").attr('class','control-group error')
                        $("#client_type").val('')
                        $("#username").val('')
                        $("#password").val('')
                        $("#user_state").html('')
                        $("#expire_date_rd").val('')
                        $("#last_login").val('')
                    }                
        }); 

    
    }
    
    $("#main_form").fadeIn(800)
    $(".span3").hide()
    $(".span9").attr("class","")
    $('#expire_date').datepicker();
    $('#submit_modify_user').click(function(){
        if( $("#client_type").val()=='微博营销'){
            client_type=0
        }
        else if( $("#client_type").val()=='SEO'){   
            client_type=1
        }
        else if( $("#client_type").val()=='SEM'){   
            client_type=2
        }
        $.getJSON("/userinfo/submit_modify_user",  
                  {user_id:$("#user_id").val(),
                  client_type: client_type,
                  username:$("#username").val(),
                  password:$("#password").val(),
                  user_state:window.document.getElementById("user_state").value,
                  expire_date_rd:$("#expire_date_rd").val()
                  },  
                   function(data){
                    if(data.status=='ok'){
                    $("#modify_user_form").fadeOut(200)
                    $("#ok").fadeIn(400)
                     }else{
                                         $("#modify_user_form").fadeOut(200)

                        $("#error").fadeIn(400)
                    }                
        }); 

    
    }); 
    $("#user_id").change(function(){
        $.getJSON("/userinfo/get_user_info",  
                  {user_id:$("#user_id").val()
                  },  
                   function(data){
                    if(data.status=='ok'){
                        $("#user_id_parent").attr('class','control-group success')
                        $("#client_type").val(data.user.client_type)
                        $("#username").val(data.user.username)
                        $("#password").val(data.user.password)
                        $("#user_state").html(data.user.user_state)
                        $("#expire_date_rd").val(data.user.expire_date)
                        $("#expire_date_rd").attr('data-date',data.user.expire_date)
                        $("#last_login").val(data.user.last_login)
            
                    }else{
                        $("#user_id_parent").attr('class','control-group error')
                        
                    }                
        }); 
    })
});

