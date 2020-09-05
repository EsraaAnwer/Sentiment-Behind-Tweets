

$(document).ready(function(){

$('.pie_chart').removeClass('img_style');
  $('.pie_chart').attr("src",'');

    $('.home_page .user_input_form .submit_btns .submit_text').click(function(e){

        e.preventDefault(); // prevent default action of form submitted
          $(".account_name span").empty();
        // $(".tweets_classifcation_result").empty();
        $(".tweets_classifcation_result .Tweet_text").empty();
        $(".tweets_classifcation_result .Tweet_text").removeClass("Tweet_text");
         // $('.pie_chart').empty();
        // $('.pie_chart').attr("src",'');
        $('#reviews_pic_chart').empty();
        $('.home_page .user_input_form .error_input').empty();
        $(".home_page .user_input_form .predicted_review").empty();
        $('.home_page .user_input_form .error_input').empty();
        $(".home_page .user_input_form .predicted_review").empty();
       
        if($('.home_page .user_input_form textarea').val() == ''){
          $('.home_page .user_input_form .error_input').addClass('error_message');
          $('.home_page .user_input_form .error_input').append("Please Enter Text");

          
        }else{
          $('.home_page .user_input_form .error_input').removeClass('error_message'); 

        }

         var user_text                   = $('.home_page .user_input_form textarea').val(),
          csrfmiddlewaretoken         = $(".home_page .user_input_form").find('input[name="csrfmiddlewaretoken"]').val(),
          language_selected               = document.querySelector('input[name="language_selected"]:checked').value;
        $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
              'user_text': user_text,
              'language_selected': language_selected,
            }),
            success: function (data) {
                if(data['Polarity'] == "Negative"){
                  $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>Tweet Text:</span> " + user_text + " <span class=\"Tweet_Class\">Tweet Class: <span style='color:#1f77b4; font-size: 18px;' >" + data['Polarity']  + "</span></span></p>");
                  // $(".tweets_classifcation_result").append("<p class=\"Tweet_text\">You Tweet is a " + data['Polarity'] + " Tweet</p");
                  // $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>You Tweet is a </span>  <span class=\"Tweet_Class\">Tweet Class: <span style='color:#2ca02c; font-size: 18px;' >" + data['Polarity']+ "</span></span></p>");
                    // $(".home_page .user_input_form .submit_btns").after("<p class=\"predicted_review\">You Review is a <span class=\"negative\">"+ data['Polarity']  +" Review</span> </p>");
                }else if (data['Polarity'] == "Positive"){
                  $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>Tweet Text:</span> " + user_text + " <span class=\"Tweet_Class\">Tweet Class: <span style='color:#2ca02c; font-size: 18px;' >" + data['Polarity']  + "</span></span></p>");

                  // $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>You Tweet is a </span>  <span class=\"Tweet_Class\">Tweet Class: <span style='color:#2ca02c; font-size: 18px;' >" + data['Polarity']+ "</span></span></p>");
                  // $(".tweets_classifcation_result").append("<p class=\"Tweet_text\">You Tweet is a " + data['Polarity'] + " Tweet</p");
                    // $(".home_page .user_input_form .submit_btns").after("<p class=\"predicted_review\">You Review is a <span class=\"positive\">"+ data['Polarity']  +" Review</span> </p>");
                }else{
                  $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>Tweet Text:</span> " + user_text + " <span class=\"Tweet_Class\">Tweet Class: <span style='color:#ff7f0e; font-size: 18px;' >" + data['Polarity']  + "</span></span></p>");

                  // $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>You Tweet is a </span>  <span class=\"Tweet_Class\">Tweet Class: <span style='color:#2ca02c; font-size: 18px;' >" + data['Polarity']+ "</span></span></p>");
                  // $(".tweets_classifcation_result").append("<p class=\"Tweet_text\">You Tweet is a " + data['Polarity'] + " Tweet</p");
                  
                }
              
            }
        })
      
  })

       $('.home_page .user_input_form .submit_btns .twitter_account').click(function(e){

        e.preventDefault(); // prevent default action of form submitted

        $(".account_name span").empty();
        // $(".tweets_classifcation_result").empty();
        $(".tweets_classifcation_result .Tweet_text").empty();
        $(".tweets_classifcation_result .Tweet_text").removeClass("Tweet_text");
         // $('.pie_chart').empty();
        // $('.pie_chart').attr("src",'');
        $('#reviews_pic_chart').empty();
        $('.home_page .user_input_form .error_input').empty();
        $(".home_page .user_input_form .predicted_review").empty();
       
        if($('.home_page .user_input_form textarea').val() == ''){
          $('.home_page .user_input_form .error_input').addClass('error_message');
          $('.home_page .user_input_form .error_input').append("Please Enter Text");

          
        }else{
          $('.home_page .user_input_form .error_input').removeClass('error_message'); 

        }

          var twitter_account                   = $('.home_page .user_input_form textarea').val(),
          csrfmiddlewaretoken         = $(".home_page .user_input_form").find('input[name="csrfmiddlewaretoken"]').val(),
          language_selected               = document.querySelector('input[name="language_selected"]:checked').value;
        $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
              'twitter_account': twitter_account,
              'language_selected': language_selected,
            }),
            success: function (data) {
                 var img = document.createElement('img'); 
                 img.className = "pie_chart";
                  img.src = "static/images/charts/" + twitter_account + ".png";
                  document.getElementById('reviews_pic_chart').appendChild(img);
              $(".tweets_classifcation_result .Tweet_text").addClass("Tweet_text");
              $(".account_name span").append("<span style=\"color: green; font-size:20;\">"  + twitter_account + "</span>");
            
             for (key in data['tweets']) {
                for (key_2 in data['tweets'][key]) {
                  if(data['tweets'][key][key_2][1] == "Positive"){
                     $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>Tweet Text:</span> " + data['tweets'][key][key_2][0] + " <span class=\"Tweet_Class\">Tweet Class: <span style='color:#2ca02c; font-size: 18px;' >" + data['tweets'][key][key_2][1]  + "</span></span></p>");
                   }else if(data['tweets'][key][key_2][1] == "Negative"){
                    $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>Tweet Text:</span> " + data['tweets'][key][key_2][0] + " <span class=\"Tweet_Class\">Tweet Class: <span style='color:#1f77b4; font-size: 18px;' >" + data['tweets'][key][key_2][1]  + "</span></span></p>");
                   }else{
                    $(".tweets_classifcation_result").append("<p class=\"Tweet_text\"><span>Tweet Text:</span> " + data['tweets'][key][key_2][0] + " <span class=\"Tweet_Class\">Tweet Class: <span style='color:#ff7f0e; font-size: 18px;' >" + data['tweets'][key][key_2][1]  + "</span></span></p>");
                   }
                 
                }
                
            }              
            }
        })
      
  })

});
 
/*----------------------- End home_page user_input_anaysis Section -----------------------------*/



/*----------------------- New -----------------------------*/



$(document).ready(function(){
  $(".login_page .login_form .submit_login").click(function (e){
    e.preventDefault();
     var username    = $('.login_page .login_form').find('input[name="username"]').val(),
     password    = $('.login_page .login_form').find('input[name="password"]').val(),
      csrfmiddlewaretoken   = $(".login_page .login_form").find('input[name="csrfmiddlewaretoken"]').val();
      $('.login_page .login_error').empty();
      $('.login_page .login_error').removeClass('alert alert-danger');
    $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
              'username': username,
              'password': password,

              }),
            success: function (data) {

              if(data['username']){
                window.location.href = "http://localhost:8000";
              }else{
                if(!username || !password){
                  $('.login_page .login_error').append("Please fill your data");
                  $('.login_page .login_error').addClass('alert alert-danger');

                }else{
                  $('.login_page .login_error').addClass('alert alert-danger');
                  $('.login_page .login_error').append("You do not have an account with this e-mail");
                }
              }
              
            }
        })
  })


  /*----------------------------------------------------------------*/

  $(".signup_page .signup_form .submit_form").click(function (e){
    e.preventDefault();
     var first_name    = $('.signup_page .signup_form').find('input[name="first_name"]').val(),
      last_name    = $('.signup_page .signup_form').find('input[name="last_name"]').val(),
      username    = $('.signup_page .signup_form').find('input[name="username"]').val(),
      password1    = $('.signup_page .signup_form').find('input[name="password1"]').val(),
      password2    = $('.signup_page .signup_form').find('input[name="password2"]').val(),
      csrfmiddlewaretoken   = $(".signup_page .signup_form").find('input[name="csrfmiddlewaretoken"]').val();
      $('.signup_page .signup_error').removeClass('alert alert-danger');
      $('.signup_page .signup_error').empty();
    
        $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
              'first_name': first_name,
              'last_name': last_name,
              'username': username,
              'password1': password1,
              'password2': password2,
              'csrfmiddlewaretoken': csrfmiddlewaretoken,

              }),
            success: function (data) {
              if(data['errors']){
                if(!first_name || !username || !password1 || !password2) {
                  $('.signup_page  .signup_error').append("Fill Your data please");
                        $('.signup_page  .signup_error').addClass('alert alert-danger');
                }else{
                  $('.signup_page  .signup_error').append("Invalid E-mail or password matching");
                }     $('.signup_page  .signup_error').addClass('alert alert-danger');
              }else{
                window.location.href = "http://localhost:8000";
              }
              

            }
        })
  })


   $(".contact_us_page .contact_us_form .submit_contact").click(function (e){
        e.preventDefault();
         var message    = $('.contact_us_page .contact_us_form').find('textarea[name="message"]').val(),
         phonenumber    = $('.contact_us_page .contact_us_form').find('input[name="phonenumber"]').val(),
         mail    = $('.contact_us_page .contact_us_form').find('input[name="mail"]').val(),
         first_name    = $('.contact_us_page .contact_us_form').find('input[name="first_name"]').val(),
        csrfmiddlewaretoken   = $(".contact_us_page .contact_us_form").find('input[name="csrfmiddlewaretoken"]').val();
        $(".contact_us_page .submit_contact_error").hide();
        if(!message || !phonenumber){
            $(this).before("<p class=\"submit_contact_error\">Please complete form data</p>");
        }else{
            var email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i,
            phonenumber_regex = /[0-9]/;
            if(!email_regex.test(mail) && mail){
            $(this).before("<p class=\"submit_contact_error\">this is not valid email</p>");
            }else if(!phonenumber_regex.test(phonenumber) && phonenumber){
                 $(this).before("<p class=\"submit_contact_error\">This is not valid phone number valid number as 01116259370 with 11 number</p>");
            }else{
                 $.ajax({
            url: '', 
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfmiddlewaretoken,
            },
            data: JSON.stringify({
                'message': message,
                'phonenumber': phonenumber,
                'mail': mail,
                'first_name': first_name,
                }),
            success: function (data) {
               
               window.location.href = "http://localhost:8000";
                }
            })

            }
        }
        
       
    })

})
