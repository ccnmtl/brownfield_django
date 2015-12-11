/* Putting Mixins to use for validation in multiple views here */

// A simple object with some methods
var ValidationMixin = {
    onlyLetters: function (check_string) {

         // It will have the context of the main class
         console.log('Context = ', this);
         alert(check_string);
         //var TCode = document.getElementById('TCode').value;
         if( /[^a-zA-Z]/.test(check_string) ) {
            alert('Please only enter letters for first and last names');
            return false;
         }
         return true;  
    },
    
    onlyAlphaNumeric: function (check_string){
        alert(check_string);
        //var TCode = document.getElementById('TCode').value;
        if( /[^a-zA-Z0-9]/.test(check_string) ) {
           alert('Please only enter letters for first and last names');
           return false;
        }
        return true;     
    },
    
    onlyIntegers: function (check_string) {

        alert(check_string);
        //var TCode = document.getElementById('TCode').value;
        if( /[^0-9]/.test(check_string) ) {
           alert('Please only enter letters for first and last names');
           return false;
        }
        return true; 
        
    }

};
