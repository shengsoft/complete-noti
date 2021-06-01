$(() => {

    var socket = io.connect('http://' + document.domain + ':' + location.port)
    var clientArray = []
    var client = []
    var count = 0
    var clientID 

    function play_sound(sound_clip) {
        var soundElement = document.createElement('audio')
        soundElement.setAttribute('src', sound_clip)
        soundElement.play()
    }

    if(location.pathname === '/dashboard/chat') {
        $('.content').hide() 
      } 







      //var url = window.location.search;
      //url = url.replace("?", ''); // remove the ?
      





      /*
      If you're a logged in client and there are new messages OR youre not on the chat page 
      send a notification alert
    */

   

    $('.client-list').on('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        clientID = $(e.currentTarget).attr('data-id');
        var clientName = $(e.currentTarget).attr('data-client');
        var clientImage = $(e.currentTarget).find('img').attr('src');
        payeeID = document.querySelector('#admin').getAttribute('data-admin-id');
        var payee = document.querySelector('#admin').getAttribute('data-admin_username');
        $('.chat').show()
        $('.message-bubble').remove() 
        clientArray.push(clientID, clientName)
        
        for(let i = 0; i < client.length; i++) { 
            if(client[i].room === clientID) {
                $('.message-bubble').show() 
                client[i].message.forEach((mesg) => {
                $('.message-box').append(`<div class="message-bubble">${mesg}</div>`).show()
                 })
                
            } 

        }
        
        $('.content').hide()
         if(clientImage == '' || clientImage == undefined){
            $('#chat-toolbar').html(`<i class="fas fa-user-circle"></i><span>${clientName}</span>`) 
         } else {
            $('#chat-toolbar').html(`<img src='${clientImage}' alt='${clientImage}'/><span>${clientName}</span>`)
         } 

         // join room whenever select client
        socket.emit('join-room', {'room' : clientID})
        //socket.emit('chat-active', {'payee_id' : payeeID})

     })
    



    socket.on('connect', (e) => {
        if(location.pathname === '/dashboard') {
            payeeID = document.querySelector('#admin').getAttribute('data-admin-id');
            socket.emit('join-room', {'room' : payeeID})
            console.log('added by payee')
         } 
    //    if(clientID != null) {
    //         clientID = document.querySelector('#client-chat').getAttribute('data-id');
    //         socket.emit('join-room', {'room' : clientID, 'client' : 1})
    //         console.log('new user connected', clientID)
    //     }

    })

    socket.on('notification-alert', (alert) => {
        if(alert.user == 'client') {
             $('.notification').remove()
             $('.payee-notification-alert').append(`<span class="notification">${alert.count}</span>`)
  
        }   else {
             $('.notification').remove()  
             $('.notification-alert').append(`<span class="notification">${alert.count}</span>`)
        }
      })
  
  
      socket.on('chat-history', (list) => {
          console.log("Chat History", list);
          data = JSON.parse(list[0]);
          var messages = data.messages;
          $('.message-box').empty();
          for(i = 0; i < messages.length; i++)
          {
              var msg = messages[i];
              $('.message-box').append(`<div class="message-bubble">${msg.message}</div>`);
          }
      });



    //toolbar clicks
    
    // $('#dashboard-toolbar ul li a').on('click', (e) => {
    //     socket.disconnect()
    // })
    
    //get history when you click the chat button
    $('#chat-panel').on('click', (e) => {
        //get chat history
        payeeID = document.querySelector('#admin').getAttribute('data-admin-id')
        socket.emit('chat-active', {'payee_id' : payeeID})
    })


    $('.dashboard-logo a').on('click', (e) => {
       //get chat history
    })
    
    
     $('#chat-message').keyup(function(event) {
          event.preventDefault()  
          payee = document.querySelector('#admin').getAttribute('data-admin_username');
          payeeID = document.querySelector('#admin').getAttribute('data-admin-id');
          roomId = clientArray[clientArray.length - 2]
          clientName = clientArray[clientArray.length - 1]
    
          if (event.which === 13) {
             var message = $('#chat-message').val()
              socket.emit('payeepro-chat', {
                username: clientName,
                room: roomId,
                payee: payee,
                payee_id: payeeID,
                message: message 
              })             

         }

    
     })




  /***  END OF PAYEE */

        $('#client-chat-message').keyup(function(event) {
            event.preventDefault() 
            client = document.querySelector('#client-chat').getAttribute('data-client');
            clientID = document.querySelector('#client-chat').getAttribute('data-id');
            payeeID = document.querySelector('#client-chat').getAttribute('data-payee-id')
            payee = document.querySelector('#client-chat').getAttribute('data-payee');

        
            if (event.which === 13) {
                var mesg = $('#client-chat-message').val()
                socket.emit('payeepro-client-chat', {
                    username: client,
                    room: clientID,
                    payee: payee,
                    payee_id: payeeID,
                    message: mesg 
                })     
                
                //notification sent
                // socket.emit('notifications', () => {
                //     $('#notification-alert').append('<div id="notification"></div>')
                // })
            
            }
            
            
        })


        socket.on('client-response', (msg) => {
           play_sound('/static/sound/sms-alert-3-daniel_simon.mp3')
           $('#client-chat-message').val('')
    
          socket.emit('notifications', {'count' : count + 1, 'user' : 'client', 'name' : msg.username})
           
           $('.message-box').append(`<div class="message-bubble">${msg.message}</div>`).show()
        })


    
    /***  END */
    




    
    
    // socket.on('disconnect', () => {
    //     //get chat history from the database
    //     // $.ajax({
    //     //     url: '/dashboard/messages',
    //     //     type: 'GET',
    //     //     data: JSON.stringify({data: data}),
    //     //      contentType: 'application/json',
    //     //      dataType: 'json',
    //     //      success: (response) => {
    //     //         console.log(response)
    //     //     }
    //     // })
    //     //then populate all html elements applicable with the chat history
    //     console.log('Test these nuts')
    // })
    


     socket.on('response', (msg) => {
        play_sound('/static/sound/sms-alert-3-daniel_simon.mp3')
        $('#chat-message').val('')
        socket.emit('notifications', {'count' : count + 1, 'user' : 'payee', 'name' : msg.payee})
        var clients = {
            name: msg.username, 
            room: msg.room, 
            payee: msg.payee, 
            message: [msg.message]
        } 

        $('.message-box').append(`<div class="message-bubble">${msg.message}</div>`).show()
        
        if(typeof client !== 'string' || client instanceof String){
            if(client.filter(client => client.name === msg.username).length > 0) {
                for(var i = 0; i < client.length; i++) {
                    if(client[i].name === msg.username){
                        client[i].message.push(msg.message)      
                    }
                }      
            
                }  else {
                    client.push(clients)
                }
            
        }
    
      })



      /** client chat  */
    






    
    
    })
    
    
    
    
    
    
    