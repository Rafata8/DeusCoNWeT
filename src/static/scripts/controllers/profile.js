'user strict'
angular.module('picbit')

.controller('ProfileCtrl', function ($scope) {
	
	$scope.calC= function()	{
    
	var nombre=document.getElementById("nombre").value;
	var apellido=document.getElementById("apellido").value;
	var mail=document.getElementById("sender").value;	
    var dia=document.getElementById("dia").selectedItemLabel;
    var mes=document.getElementById("mes").selectedItemLabel;
    var ano=document.getElementById("ano").selectedItemLabel;
    var sex=document.getElementById("sex").selectedItemLabel;
		console.log(nombre);
		console.log(apellido);
		console.log(mail);
        console.log(sex);
        console.log(dia);
        console.log(mes);
        console.log(ano);
		
    };
	
	  $scope.takeInfoLog = function(e){
		  
		  if (e.detail.redSocial === 'googleplus') {
			  var googleplus="googleplus";
              var acToken=e.detail.token;
            
		  }
		  if (e.detail.redSocial === 'facebook') {
			  var facebook="facebook";
              var acToken=e.detail.token;
              var userId=e.detail.userId;
		  }
		  if (e.detail.redSocial === 'github') {
				var github="github";
                var acToken=e.detail.token;
   				console.log("github");
  
		  }
		  if (e.detail.redSocial === 'linkedin') {
				var linkedin="linkedin";
                var acToken=e.detail.token;
                var userId=e.detail.userId;
                console.log("linkedin");
                
  
		  }
		  if (e.detail.redSocial === 'instagram') {
				var instagram="instagram"
                var acToken=e.detail.token;
                var userId=e.detail.userId;
   				console.log("instagram");

		  }
		  if (e.detail.redSocial === 'twitter') {
				var twitter="twitter";
                var acToken=e.detail.token;
   				console.log("twitter")
 
 
		  }
	
		  };

  document.getElementById("pr").addEventListener('google-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('facebook-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('linkedin-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('github-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('instagram-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('twitter-logged',$scope.takeInfoLog);




})

