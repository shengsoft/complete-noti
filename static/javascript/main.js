

$(() => {
    


//this needs the client id and the document to print
function printPDF(documentType, id){
    var param = '/dashboard/print/pdf/'
    param += documentType + '/'
    param += id
    $('#generate-report-button').attr('href', param)
 }
 

 function printSpreadsheet(documentType, id){
    var param = '/dashboard/spreadsheet/'
    param += documentType + '/'
    param += id
    $('#generate-spreadsheet-button').attr('href', param)
 }


    
        // var id = document.querySelector('.monthly-statement').getAttribute('data-id')
        // $.ajax({
        //     url: `/dashboard/print/record/${id}`,
        //     type: 'GET',
        //     contentType: 'application/json',
        //     dataType: 'json',
        //     success: (data) => {
        //        //console.log(data)
        //        //window.location = '/d/'
    
        //     }
     
        // })

    
    /** Chat room */






   /* end */ 

   $('#login-button').on('click', (e) => {
       e.preventDefault()
       $('body').append('<div id="overlay">\
                         <div id="login-form">\
                            <h3>Log in</h3>\
                            <form>\
                              <input type="email" id="email" name="email" placeholder="E-mail" required>\
                              <button id="login">Get code to log in</button>\
                              <button id="register">Register for account</button>\
                            </form>\
                          </div>\
                          <a href="#" id="close">[X]close</a>\
                       </div>')  

                $('#close').on('click', (e) => {
                    $('#overlay, #login-form').fadeOut()
                })        


                $('#login').on('click', (e) => {
                    e.preventDefault()
                    var email = $('#email').val()
                    if(!$('#email').val() == '') {
                        $.ajax({
                            type: 'POST',
                            url: '/email_verification',
                            data: JSON.stringify({email : email}),
                            dataType: 'json',
                            contentType: "application/json",
                            success: (response) => {
                                console.log(response)
                            },
                            error: (e) => {
                                console.log(e)
                            }
                        })

/********************* */


                        $('#login-form').html('\
                        <h3>Log in</h3>\
                        <p>To sign in please enter the code sent to your email</p>\
                          <form>\
                               <input type="text" id="passcode" name="passcode" placeholder="Code" required>\
                               <button id="passcode-login">Log in with code</button>\
                               <button id="register">Register for account</button>\
                       </form>')

                
                      $('#passcode-login').on('click', (e) => {
                          e.preventDefault()
                          var passcode = $('#passcode').val()
                          if(!$('#passcode').val() == '') {
                            $.ajax({
                                type: 'POST',
                                url: '/passcode',
                                data: JSON.stringify({passcode: passcode}),
                                dataType: 'json',
                                contentType: "application/json",
                                success: (response) => {
                                        window.location.href = response.redirect
                                    
                                }
                            })
                          $('#login-form').html('\
                          <h3>Log in</h3>\
                          <p>Please enter the passcode provided in your email</p>\
                          <form>\
                              <input type="text" id="passcode" name="passcode" placeholder="Code" required>\
                              <button id="passcode-login">Log in with code</button>\
                              <button id="register">Register for account</button>\
                          </form>')

                       } else {
                            $('#passcode').css({'background' : '#ccc', 'border' : '2px solid blue', 'color' : '#000'})
                        }

                    })
                   
                   
                
/*************************** */

                    } 
                    
                    
                    else {
                        $('#email').css({'background' : '#ccc', 'border' : '2px solid blue', 'color' : '#000'})
                     
                    }
            
            
                 })   

/* registration */
                 $('#register').on('click', (e) => {
                    e.preventDefault()
                    $('#login-form').remove()
                    $('#close').remove()
                    $('body').append('<div id="overlay">\
                        <div id="registration">\
                        <h3>Registration</h3>\
                        <form method="post" id="registration-form">\
                            <input type="text" name="first-name" placeholder="First name" id="registration-first-name" required>\
                            <input type="text" name="middle-name" placeholder="Middle Name(if you have one)" id="registration-middle-name" value="n/a">\
                            <input type="text" name="last-name" placeholder="Last name" id="registration-last-name" required>\
                            <input type="email" name="email" placeholder="E-mail" id="registration-email" required>\
                            <input type="submit" id="registration-submit" value="Register for an account">\
                            <button id="registration-close">Close</button>\
                        </form>\
                    </div></div>')

                    $('#registration-close').on('click', (e) => {
                        e.preventDefault()
                        $('#overlay, #registration').fadeOut()
                    })

                    $('#registration-submit').on('click', (e) => {
                        e.preventDefault()
                        var registrationFirstName = $('#registration-first-name').val()
                        var registrationMiddleName = $('registration-middle-name').val()
                        var registrationLastName = $('#registration-last-name').val()
                        var registrationEmail = $('#registration-email').val()
                        if(!$('#registration-first-name').val() == '' &&  !$('#registration-middle-name').val() == '' &&  !$('#registration-last-name').val() == '' && !$('#registration-email').val() == '') {
                            $.ajax({
                                type: 'POST',
                                url: '/register',
                                data: JSON.stringify({
                                        first_name : registrationFirstName,
                                        middle_name : registrationMiddleName,
                                        last_name : registrationLastName, 
                                        email : registrationEmail
                                }),
                                dataType: 'json',
                                contentType: "application/json",
                                success: (response) => {
                                    //location: reload();
                                    console.log(response)
                                },
                                error: (e) => {
                                    console.log(e)
                                }
                            })
                       
    
    /********************* */
    

                        /* beginning of passcode form */
                        $('#registration').remove() 
                        $('#login-form').remove()
                        $('#close').remove()
                        $('#overlay').remove()
                        $('body').append('<div id="overlay">\
                           <div id="login-form">\
                            <h3>Log in</h3>\
                            <p>To sign in please enter the code sent to your email</p>\
                            <form>\
                                <input type="text" id="passcode" name="passcode" placeholder="Code" required>\
                                <button id="passcode-login">Log in with code</button>\
                                <button id="register">Register for account</button>\
                        </form>')


                                        
                      $('#passcode-login').on('click', (e) => {
                        e.preventDefault()
                        var passcode = $('#passcode').val()
                        if(!$('#passcode').val() == '') {
                          $.ajax({
                              type: 'POST',
                              url: '/passcode',
                              data: JSON.stringify({passcode: passcode}),
                              dataType: 'json',
                              contentType: "application/json",
                              success: (response) => {
                                      window.location.href = response.redirect
                                  
                              }
                          })
                        $('#login-form').html('\
                        <h3>Log in</h3>\
                        <p>Please enter the passcode provided in your email</p>\
                        <form>\
                            <input type="text" id="passcode" name="passcode" placeholder="Code" required>\
                            <button id="passcode-login">Log in with code</button>\
                            <button id="register">Register for account</button>\
                        </form>')

                     

                    } else {
                        $('#passcode').css({'background' : '#ccc', 'border' : '2px solid blue', 'color' : '#000'})
                    }
                    
                        /** end of passcode form  */

                    })
                }

            })
            
       })  
    /******************* */            
                

          }) //end of login form


/** contact form  */

$('#contact-form').on('click', (e) => {
    e.preventDefault()
    var name  = $('#contact-name').val()
    var email = $('#contact-email').val()
    var subject = $('#contact-subject').val()
    var message = $('#contact-message').val() 
    $('body').append('<div id="overlay">\
        <div id="alert-message">\
           <h3>Thank you</h3>\
           <p>We appreciate your interest in Payee Pro. We will be in contact with you shortly.</p>\
               <button id="close-alert-box">OK</button>\
           </div>\
        </div>')

       $('#close-alert-box').on('click', (e) => {
           $('#alert-message, #overlay').fadeOut(2000)
           $('.contact form').trigger('reset');

       })

       $.ajax({
           url: '/contact',
           type: 'POST',
           data: JSON.stringify({
                 name  : name,
                 email : email,
                 subject : subject,
                 message : message

           }),
           dataType: 'json',
           contentType: "application/json",
           success: (response) => {
               console.log(response)
           }
       })
 })

 /********************* */


$('nav div').on('click', (e) => {
    $('body').append('<div id="small-menu-panel">\
    <div id="close-window">X</div>\
    <ul>\
      <li><a href="#" title="home">home</a></li>\
      <li><a href="#" title="services">services</a></li>\
      <li><a href="#" title="contact">contact</a></li>\
      <li><a href="#" title="subscribe">subscribe</a></li>\
    </ul>\
    </div>').slideToggle()
})

 /************ */

 $('.payee-email button').on('click', (e) => {
     e.preventDefault()
     var email = $('#email').val()
     var subject = $('#email-subject').val()
     var message = $('#email-message').val()
     $.ajax({
         url: '/dashboard/send/email',
         type: 'POST',
         data: JSON.stringify({
              email : email,
              subject : subject,
              message : message
         }),
         contentType: 'application/json',
         dataType: 'json',
         success: (response) => {
             console.log(response)
         }

     })

     $('body').append('<div id="overlay">\
     <div id="budget-alert-message">\
      <div id="budget-message">\
        <h3>Great! &#129395;&#127881;</h3>\
        <p>Your message has been sent</p>\
      </div></div></div>')
   
   setTimeout(() => {
       $('.payee-email form').trigger('reset');
       $('#overlay').fadeOut() 
       $('#budget-alert-message').fadeOut()
   }, 5000)
 })


$('.client').on('click', (e) => {
   e.preventDefault() 
   e.stopPropagation();
   var id = $(e.currentTarget).attr('data-id');
   document.querySelector('.monthly-statement').setAttribute('data-id', id)
   document.querySelector('.annual-statement').setAttribute('data-id', id)
   document.querySelector('.chat-history').setAttribute('data-id', id)   
})

$('.monthly-statement').on('click', (e) => {
     e.preventDefault() 
     e.stopPropagation();
     var monthlyReport = $(e.currentTarget).attr('class')
     var id = document.querySelector('.monthly-statement').getAttribute('data-id')
     document.querySelector('#print-report-button').setAttribute('report-type', monthlyReport)
     document.querySelector('#generate-report-button').setAttribute('report-type', monthlyReport)
     document.querySelector('#generate-spreadsheet-button').setAttribute('report-type', monthlyReport)
     printPDF(monthlyReport, id)
     $('.monthly-statement h1').css('color', '#fafafa')
     $('.monthly-statement').css('background', '#34925E')
     $('.chat-history, .annual-statement').css({'background' : 'transparent'})
     $('.chat-history h1, .annual-statement h1').css({'color' : '#000'})
})

$('.annual-statement').on('click', (e) => {
    e.preventDefault() 
    e.stopPropagation();
    var annualReport = $(e.currentTarget).attr('class')
    var id = document.querySelector('.monthly-statement').getAttribute('data-id')
    document.querySelector('#print-report-button').setAttribute('report-type', annualReport)
    document.querySelector('#generate-report-button').setAttribute('report-type', annualReport)
    document.querySelector('#generate-spreadsheet-button').setAttribute('report-type', annualReport)
    printPDF(annualReport, id)
    $('.annual-statement h1').css('color', '#fafafa')
    $('.annual-statement').css('background', '#34925E')
    $('.chat-history, .monthly-statement').css({'background' : 'transparent'})
    $('.chat-history h1, .monthly-statement h1').css({'color' : '#000'})
})


$('.chat-history').on('click', (e) => {
    e.preventDefault() 
    e.stopPropagation();
    var chatHistory = $(e.currentTarget).attr('class')
    var id = document.querySelector('.monthly-statement').getAttribute('data-id')
    document.querySelector('#print-report-button').setAttribute('report-type', chatHistory)
    document.querySelector('#generate-report-button').setAttribute('report-type', chatHistory)
    document.querySelector('#generate-spreadsheet-button').setAttribute('report-type', chatHistory)
    printPDF(chatHistory, id)
    $('.chat-history h1').css('color', '#fafafa')
    $('.chat-history').css('background', '#34925E')
    $('.annual-statement, .monthly-statement').css({'background' : 'transparent'})
    $('.annual-statement h1, .monthly-statement h1').css({'color' : '#000'})
})




$('#print-report-button').on('click', (e) => {
    //which report to print
    //e.preventDefault()
    //e.stopPropagation();
    var printDocumentType = document.querySelector('#print-report-button').getAttribute('report-type')
    var id = document.querySelector('.monthly-statement').getAttribute('data-id')   

    if(printDocumentType == null) {
        console.log('a client wasnt selected')
    }
    
    if(printDocumentType == 'chat-history') {
         console.log(printDocumentType)
       // create route for chat history print report and pass it the client id to get the chat history
       //send id of the user
        $('#print-document').load('/dashboard/print/chat-history/'+id, () => {
                var printContent = document.getElementById('print-document')
                var win = window.open('', '', 'width=900,height=650')
                win.document.write(printContent.innerHTML)
                win.document.close()
                win.focus()
                win.print()
                win.close()
        })

    } else if(printDocumentType == 'monthly-statement' || printDocumentType == 'annual-statement'){

            //send id of the user
            $('#print-document').load('/dashboard/print/'+id, () => {
                var printContent = document.getElementById('print-document')
                var win = window.open('', '', 'width=900,height=650')
                win.document.write(printContent.innerHTML)
                win.document.close()
                win.focus()
                win.print()
                win.close()
        })
    
     }
    

   //load page to print


})


$('#generate-report-button').on('click', (e) => {
    //e.preventDefault()
    var printDocumentType = document.querySelector('#print-report-button').getAttribute('report-type')
    var id = document.querySelector('.monthly-statement').getAttribute('data-id')
    console.log(printDocumentType)
    console.log(id)
    printPDF(printDocumentType, id)
    // if(printDocumentType == null) {
    //     console.log('a client wasnt selected')
    // } else {
    //     printPDF(printDocumentType, id)
    // }

}) 


$('#generate-spreadsheet-button').on('click', (e) => {
    //var id = document.querySelector('.monthly-statement').getAttribute('data-id')
    var printDocumentType = document.querySelector('#print-report-button').getAttribute('report-type')
    var id = document.querySelector('.monthly-statement').getAttribute('data-id')
    if(printDocumentType == null) {
        console.log('a client wasnt selected')
     } else {
        printSpreadsheet(printDocumentType, id)
     }

})


$('.client').on('click', (e) => {
    //e.preventDefault()
   $(e.currentTarget).css({'background' : 'rgba(0, 199, 140, 0.5)'})
   $('.client').not(e.currentTarget).css({'background' : 'transparent'})
})


    
})