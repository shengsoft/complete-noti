$(() => {

var socket = io.connect('http://' + document.domain + ':' + location.port);


/* budget *****/
var expenses = $('.expenses')
var amounts = $('.expense_amount')
var incomeSources = $('.income-source')


$('#save-budget-items').on('click', (e) => {
   e.preventDefault()
   var firstName = $('#client-first-name').val()
   var middleName = $('#client-middle-name').val()
   var lastName = $('#client-last-name').val()
   var email = $('#client-email').val()
   var ssn = $('#client-ssn').val()
   var dob = $('#dob').val()
   var budgetAmount = $('#budget_amount').val()
   var firstExpense = $('#expenses_1').val()
   var firstExpenseAmount = $('#amount_1').val()
   var secondExpense = $('#expenses_2').val()
   var secondExpenseAmount = $('#amount_2').val()
   var thirdExpense = $('#expenses_3').val()
   var thirdExpenseAmount = $('#amount_3').val()
   var fourthExpense = $('#expenses_4').val()
   var fourthExpenseAmount = $('#amount_4').val()
   var fifthExpense = $('#expenses_5').val()
   var fifthExpenseAmount = $('#amount_5').val()
   var budgetArray = []  
   budget = {
        first_name : firstName,
        middle_name : middleName,
        last_name : lastName,
        email : email,
        ssn : ssn,
        dob : dob,
        budget_amount : budgetAmount,
        first_expense : firstExpense,
        first_expense_amount : firstExpenseAmount,
        second_expense : secondExpense,
        second_expense_amount : secondExpenseAmount,
        third_expense : thirdExpense,
        third_expense_amount : thirdExpenseAmount,
        fourth_expense : fourthExpense,
        fourth_expense_amount : fourthExpenseAmount,
        fifth_expense : fifthExpense,
        fifth_expense_amount : fifthExpenseAmount,
        additional_expenses : []

   }



//budgetArray.push(budget)





function generateFields(name, value, i){
   if(i==0) {
       currentKey = 0;
       budget.additional_expenses = [];
       budget.additional_expenses.push({});
   } else if(Object.keys(budget.additional_expenses[currentKey]).length == 8) {
       currentKey++;
       budget.additional_expenses.push({});
   }
   switch(name){
       case 'income-source-name':
           item_name = "income_source_name_"+i;
           break;
       case 'income-source-amount':
           item_name = "income_source_"+i;
           break;
       case 'expense':
           item_name = "expense_"+i;
           break;
       case 'expense_amount':
           item_name = "expense_amount_"+i;
           break;            
   }
   budget.additional_expenses[currentKey][item_name]  = value 
}

let currentKey = 0;

    $("#budget form input").each(function(index){
        var input = $(this).val()
        var className = $(this).attr('class')

        if(index == 0) {
            currentKey = 0;
            budget.additional_expenses = [];
            budget.additional_expenses.push({});
        } else if(Object.keys(budget.additional_expenses[currentKey]).length == 8) {
            currentKey++;
            budget.additional_expenses.push({});
        }
   
        switch(className){
            case 'income-source-name':
               item_name = "income_source_name_"+ input           
               break;
            case 'income-source':
               item_name = "income_source_"+input
               break;
            case 'expenses':
               item_name = "expense_"+ input
               break;
            case 'expense_amount':
               item_name = "expense_amount_"+input
               break;             
          }
          budget.additional_expenses[currentKey][item_name]  = input 


      //generateFields(className[index], input[index], index)
      console.log(budget.additional_expenses)

   
      });


       // budget['additional_expenses'] = additional_expenses 

    //console.log(new_budget)


    console.log(budget)

   $.ajax({
      url: '/save_budget',
      type: 'POST',
      data: JSON.stringify({
         first_name : firstName,
         middle_name : middleName,
         last_name : lastName,
         email : email,
         ssn : ssn,
         dob : dob,
         budget_amount : budgetAmount,
         first_expense : firstExpense,
         first_expense_amount : firstExpenseAmount,
         second_expense : secondExpense,
         second_expense_amount : secondExpenseAmount,
         third_expense : thirdExpense,
         third_expense_amount : thirdExpenseAmount,
         fourth_expense : fourthExpense,
         fourth_expense_amount : fourthExpenseAmount,
         fifth_expense : fifthExpense,
         fifth_expense_amount : fifthExpenseAmount,
         additional_expenses: budget.additional_expenses
      }),
      dataType: 'json',
      contentType: 'application/json',
      success: (response) => {
          console.log(response)
      }
   })

   /**   populate sidebar with clients */
   $('body').append('<div id="overlay">\
   <div id="budget-alert-message">\
    <div id="budget-message">\
      <h3>Great! &#129395;&#127881;</h3>\
      <p>Budget has been saved</p>\
    </div></div></div>')
 
 setTimeout(() => {
     $('#budget form').trigger('reset');
     $('#overlay').fadeOut() 
     $('#budget-alert-message').fadeOut()
   }, 5000)    

  
})






$('.client-details').load('test.html')


$('#add-expenses-field').on('click', (e) => {
    e.preventDefault()
    $('#budget form').append(`\
        <input type="text"  class="income-source-name" placeholder="Income source"><br>\
        <input type="number" class="income-source-amount" placeholder="Income source... $0"><br>\
        <input type="text" class="expense" placeholder="Enter client expense">\
        <input type="number" class="expense_amount" placeholder="$0.00"><br>\
        <input type="text" class="expense" placeholder="Enter client expense">\
        <input type="number" class="expense_amount" placeholder="$0.00"><br>\
        <input type="text" class="expense" placeholder="Enter client expense">\
        <input type="number" class="expense_amount" placeholder="$0.00"><br>\
    `)
  })
})