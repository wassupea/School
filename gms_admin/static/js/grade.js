$(document).ready(function(){
  var hwView = document.getElementById('container1');
  var quizView = document.getElementById('container2');
  var swView = document.getElementById('container3');
  var examView = document.getElementById('container4');
  var performanceView = document.getElementById('container5');
  var calculateView = document.getElementById('container6');
  var review = document.getElementById('review');
  var select = document.getElementById('calculate_qtr');
  var activity = document.getElementById('select-id');
  
  $("#final_grade").prop('disabled', true);
  hwView.style.display ="None";
  quizView.style.display ="None";
  swView.style.display ="None";
  examView.style.display ="None";
  performanceView.style.display ="None";
  calculateView.style.display="None";
  select.style.display="None";
  review.style.display="None";
  
  
      $("#add_tab").click(function(e){
        activity.style.display = "Block";
        calculateView.style.display = "None";
        review.style.display = "None";
      });
      $("#review_tab").click(function(e){
        activity.style.display = "none";
        calculateView.style.display = "None";
        review.style.display ="block";
        swView.style.display= "none";
        quizView.style.display = "none";
        hwView.style.display= "none";
        examView.style.display ="none";
        performanceView.style.display ="none";
      });
      $("#calculate_tab").click(function(e){
        swView.style.display= "none";
        quizView.style.display = "none";
        hwView.style.display= "none";
        examView.style.display ="none";
        performanceView.style.display ="none";
        calculateView.style.display="Block";
        select.style.display="Block";
        activity.style.display="none";
        review.style.display = "None";
      });
  
      
      $("#activity").change(function(e){
        var selectedVal = $(this).children("option:selected").val();
  
        if (selectedVal == 1) {
        hwView.style.display= "block";
        swView.style.display ="None";
        quizView.style.display = "none";
        examView.style.display ="None";
        performanceView.style.display ="None";
        calculateView.style.display="None";
        }
        else if (selectedVal ==2 ) {
          hwView.style.display= "none";
          swView.style.display ="None";
          quizView.style.display = "block";
          examView.style.display ="None";
          performanceView.style.display ="None";
          calculateView.style.display="None";
        }
        else if (selectedVal ==3 ) {
          
          swView.style.display= "block";
          quizView.style.display = "none";
          hwView.style.display= "none";
          examView.style.display ="None";
          performanceView.style.display ="None";
          calculateView.style.display="None";
        }
        else if (selectedVal ==4 ) {
          swView.style.display= "none";
          quizView.style.display = "none";
          hwView.style.display= "none";
          examView.style.display ="block";
          performanceView.style.display ="None";
          calculateView.style.display="None";
        }
  
        else if (selectedVal ==5) {
          swView.style.display= "none";
          quizView.style.display = "none";
          hwView.style.display= "none";
          examView.style.display ="none";
          performanceView.style.display ="block";
          calculateView.style.display="None";
        }
        
      });
      $("#calculate_qtr").change(function(e){
        $('#dito' ).empty();
        document.getElementById('hw_ave_view').value = '';
        var selectedVal = $(this).children("option:selected").val();
        var student = $('#student').val()
        $.ajax({
          type: "POST",
          url: '/get_homework',
          data: {selectedVal:selectedVal, student:student},
        })
          .done(function(response){
            alert('fetched')
            var json_data = JSON.parse(response);
        
    
          var tr;
          for (i in json_data) {
          tr = $('<tr/>');
          tr.append("<td>" + json_data[i].name + "</td>");
          tr.append("<td>" + json_data[i].score+ "</td>");
          $('#dito').first().append(tr);
        } 
  
          
    
    
        })
          .fail(function(){
            alert("Error")
          })
      });
  
      $("#quiz_qtr").change(function(){
        $('#dito2' ).empty();
        document.getElementById('qz_ave_view').value = '';
        var selectedVal = $(this).children("option:selected").val();
        var student = $('#student').val()
        $.ajax({
          type: "POST",
          url: '/get_quiz',
          data: {selectedVal:selectedVal, student:student},
        })
          .done(function(response){
            alert('fetched')
            var json_data = JSON.parse(response);
    
          var tr;
          for (i in json_data) {
          tr = $('<tr/>');
          tr.append("<td>" + json_data[i].name + "</td>");
          tr.append("<td>" + json_data[i].score+ "</td>");
          $('#dito2').first().append(tr);
        } 
    
    
        })
          .fail(function(){
            alert("Error")
          })
      });
  
      $("#sw_qtr").change(function(){
        $('#dito3' ).empty();
        document.getElementById('sw_ave_view').value = '';
        var selectedVal = $(this).children("option:selected").val();
        var student = $('#student').val()
        console.log(selectedVal, student)
        $.ajax({
          type: "POST",
          url: "/get_seatwork",
          data: {selectedVal:selectedVal, student:student},
        })
          .done(function(response){
            alert('fetched');
            var json_data = JSON.parse(response);
          var tr;
          for (i in json_data) {
          tr = $('<tr/>');
          tr.append("<td>" + json_data[i].name + "</td>");
          tr.append("<td>" + json_data[i].score+ "</td>");
          $('#dito3').first().append(tr);
        } 
    
    
        })
          .fail(function(){
            alert("Error")
          })
      });
  
      
      $("#perf_qtr").change(function(){
        $('#performance_view' ).empty();
        document.getElementById('perf_ave_view').value = '';
        var selectedVal = $(this).children("option:selected").val();
        var student = $('#student').val()
        console.log(selectedVal, student)
        $.ajax({
          type: "POST",
          url: "/get_performance",
          data: {selectedVal:selectedVal, student:student},
        })
          .done(function(response){
            alert('fetched');
            var json_data = JSON.parse(response);
          var tr;
          for (i in json_data) {
          tr = $('<tr/>');
          tr.append("<td>" + json_data[i].name + "</td>");
          tr.append("<td>" + json_data[i].score+ "</td>");
          $('#performance_view').first().append(tr);
        } 
    
    
        })
          .fail(function(){
            alert("Error")
          })
      });
  
      $("#exam_qtr").change(function(){
        $('#exam_view' ).empty();
        document.getElementById('exam_ave_view').value = '';
        var selectedVal = $(this).children("option:selected").val();
        var student = $('#student').val()
        console.log(selectedVal, student)
        $.ajax({
          type: "POST",
          url: "/get_exam",
          data: {selectedVal:selectedVal, student:student},
        })
          .done(function(response){
            alert('fetched');
            var json_data = JSON.parse(response);
          var tr;
          for (i in json_data) {
          tr = $('<tr/>');
          tr.append("<td>" + json_data[i].name + "</td>");
          tr.append("<td>" + json_data[i].score+ "</td>");
          $('#exam_view').first().append(tr);
        } 
    
    
        })
          .fail(function(){
            alert("Error")
          })
      });
  
      $("#hw_calculate").click(function(e){
        e.preventDefault();
       
        var table = document.getElementById('hw_table2'), sumVal =0;
        console.log(table)
  
        for(var i =1; i < table.rows.length; i++) {
          sumVal = sumVal + parseInt(table.rows[i].cells[1].innerHTML);
          values = table.rows[i].cells[1].innerHTML;
        }
  
        var avg = sumVal / (table.rows.length - 1);
        document.getElementById('hw_ave_view').value = avg;
        
        document.getElementById('hw_ave').value = avg;
        console.log(sumVal)
  
      });
  
      $("#quiz_average").click(function(e){
        e.preventDefault();
        var table = document.getElementById('quiz_table'), sumVal =0;
  
        for(var i =1; i < table.rows.length; i++) {
          sumVal = sumVal + parseInt(table.rows[i].cells[1].innerHTML);
          values = table.rows[i].cells[1].innerHTML;
        }
  
        var avg = sumVal / (table.rows.length - 1);
        document.getElementById('qz_ave_view').value = avg;
        
        document.getElementById('qz_ave').value = avg;
  
     });
  
     $("#calculate_sw_btn").click(function(e){
    
      e.preventDefault();
      var table = document.getElementById('sw_table'), sumVal =0;
  
      for(var i =1; i < table.rows.length; i++) {
        sumVal = sumVal + parseInt(table.rows[i].cells[1].innerHTML);
        
      }
      
      var avg = sumVal / (table.rows.length - 1);
      document.getElementById('sw_ave_view').value = avg;
      document.getElementById('sw_ave').value = avg;
   });
  
   $("#calculate_perf_btn").click(function(e){
  
    e.preventDefault();
    var table = document.getElementById('perf_table'), sumVal =0;
  
    for(var i =1; i < table.rows.length; i++) {
      sumVal = sumVal + parseInt(table.rows[i].cells[1].innerHTML);
      
    }
    
    var avg = sumVal / (table.rows.length - 1);
    document.getElementById('perf_ave_view').value = avg;
    document.getElementById('performance_ave').value = avg;
  
  });
  
  $("#calculate_exam_btn").click(function(e){
  
    e.preventDefault();
    var table = document.getElementById('exam_table'), sumVal =0;
  
    for(var i =1; i < table.rows.length; i++) {
      sumVal = sumVal + parseInt(table.rows[i].cells[1].innerHTML);
      
    }
    
    var avg = sumVal / (table.rows.length - 1);
    document.getElementById('exam_ave_view').value = avg;
    document.getElementById('exam_ave').value = avg;
  
  });
  
   $("#calculate_written_btn").click(function(e){
    e.preventDefault();
    var hw_ave = $('#hw_ave').val()
    var hw_percent = $('#hw_percentage').val();
    var sw_ave = $('#sw_ave').val()
    var sw_percent = $('#sw_percentage').val();
    var qz_ave = $('#qz_ave').val()
    var qz_percent = $('#qz_percentage').val()
    var selectedVal = $('#written_qtr').val();
    var student = $('#student').val()
    var hw_qtr = $('#calculate_qtr').val();
    var qz_qtr = $('#quiz_qtr').val();
    var sw_qtr = $('#sw_qtr').val();
    var perf_qtr = $('#perf_qtr').val();
    var exam_qtr = $('#exam_qtr').val();
  
   hw_percentage = hw_percent / 100;
   sw_percentage = sw_percent / 100;
   qz_percentage = qz_percent / 100;
   
  
   total_percentage = parseInt(hw_percent)  +  parseInt(sw_percent)+ parseInt(qz_percent);


    var $foo = $(this);
    if (!$foo.data('clicked')) {
      if (hw_percent<0 || qz_percent < 0 || sw_percent <0){
        alert('Invalid');}
   
       else {
         if (total_percentage == 100) {
           if (hw_qtr == qz_qtr == sw_qtr == perf_qtr == exam_qtr) {
           hw_grade = hw_ave * hw_percentage;
           sw_grade = sw_ave * sw_percentage;
           qz_grade = qz_ave * qz_percentage;
           written_grade = hw_grade + sw_grade + qz_grade
           $('#written_ave_').first().append(written_grade);
           document.getElementById('written_ave').value = written_grade;
           }
           else {
             alert('Quarter must be the same');
           }
          }
   
           else if (total_percentage > 100 || total_percentage < 100) {
             alert("total percentage must be 100")
           }
           
       }
   
   
   
    } else {
      $('#written_ave_').empty();
      if (hw_percent<0 || qz_percent < 0 || sw_percent <0){
        alert('Invalid');}
   
       else {
        if (total_percentage == 100) {
          if (hw_qtr == qz_qtr == sw_qtr == perf_qtr == exam_qtr) {
          hw_grade = hw_ave * hw_percentage;
          sw_grade = sw_ave * sw_percentage;
          qz_grade = qz_ave * qz_percentage;
          written_grade = hw_grade + sw_grade + qz_grade
          $('#written_ave_').first().append(written_grade);
          document.getElementById('written_ave').value = written_grade;
          }
          else {
            alert('Quarter must be the same');
          }
         }
  
          else if (total_percentage > 100 || total_percentage < 100) {
            alert("total percentage must be 100")
          }
           
       }   
    }
    $foo.data('clicked', true);

 
 
  
  });
  
  $("#calculate_grade_btn").click(function(e){
    e.preventDefault();
    var written_ave = $('#written_ave').val()
    var written_percent = $('#written_percentage').val();
    var exam_ave = $('#exam_ave').val()
    var exam_percent = $('#exam_percentage').val();
    var performance_ave = $('#performance_ave').val()
    var performance_percent = $('#perf_percentage').val()
    var selectedVal = $('#all_qtr').val();
    var student = $('#student').val()
    console.log(written_ave,written_percent,exam_ave,exam_percent, performance_ave,performance_percent);
    
  var written_ave_pp = parseInt(written_ave)
  var exam_ave = parseInt(exam_ave)
  var performance_ave = parseInt(performance_ave)
   written_percentage = written_percent / 100;
   exam_percentage = exam_percent / 100;
   performance_percentage = performance_percent / 100;
  
   total_percentage = parseInt(written_percent)  +  parseInt(exam_percent)+ parseInt(performance_percent);
   console.log(total_percentage);
  
  if (total_percentage == 100) {
    written_grade = written_ave * written_percentage;
    exam_grade = exam_ave * exam_percentage;
    performance_grade = performance_ave * performance_percentage;
    subject_grade = written_grade + performance_grade + exam_grade
    console.log(subject_grade)
    $('#grade_view').first().append(subject_grade);
    $("#final_grade").prop('disabled', false);
    document.getElementById('final_grade').value = subject_grade;
  }
  
  else if (total_percentage > 100 || total_percentage < 100) {
    alert("total percentage must be 100")
  }
  
  
  });
  
  
      });