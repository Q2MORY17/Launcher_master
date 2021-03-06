$( document ).ready(function(){

  $.post('/app_disable_buttons', {
  }, function(data) {
  $("#encoders_ready").text(data.encoders_ready);
  if (data.encoders_ready === 0) {
  $('.button-encoder').css('background-color','#878787');
  }});



  $('#script_pitch_up').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_pitch_up');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_pitch_stop');
  });

  $('#script_pitch_down').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_pitch_down');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_pitch_stop');
  });

  $('#script_pitch_position').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_pitch_position', {
     pitch_position: $('input[name="pitch_position"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between 0 and 90');
     }
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });



  $('#script_rotation_right').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_rotation_right');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_rotation_stop');
  });

  $('#script_rotation_left').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_rotation_left');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_rotation_stop');
  });

  $('#script_rotation_position').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_rotation_position', {
     rotation_position: $('input[name="rotation_position"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between -180 and 180');
     }
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });



  $('#script_lift_up').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_lift_up');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_lift_stop');
  });

  $('#script_lift_down').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_lift_down');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_lift_stop');
  });

  $('#script_lift_position').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_lift_position', {
     lift_position: $('input[name="lift_position"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between 0 and 130');
     }
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });



  $('#script_launch_forwards').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_launch_forwards');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_launch_stop');
  });

  $('#script_launch_backwards').on('mousedown touchstart', function(event) {
   event.preventDefault();
   $.post('/app_launch_backwards');
 }).on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_launch_stop');
  });

  $('#script_launch_position').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_launch_position', {
     launch_position: $('input[name="launch_position"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between 0 and 111');
     }
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });



  $('#script_max_pitch').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_max_pitch', {
     max_pitch: $('input[name="max_pitch"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_min_pitch').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_min_pitch', {
     min_pitch: $('input[name="min_pitch"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_max_lift').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_max_lift', {
     max_lift: $('input[name="max_lift"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_min_lift').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_min_lift', {
     min_lift: $('input[name="min_lift"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });
  
  $('#script_case_open').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_case_open', {
     case_open: $('input[name="case_open"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_case_close').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_case_close', {
     case_close: $('input[name="case_close"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });


  $('#script_home').on('mouseup touchend', function(event) {
    event.preventDefault();
    $.post('/app_home');
   });

  $('#script_reset_encoders').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_reset_encoders');
   $('.button-encoder').css('background-color','#f44336');
  });

  $('#script_battery_voltage').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_battery_voltage', {
   }, function(data) {
   $("#voltage").text(data.voltage);
   });
   return false;
  });

setInterval(() => {
  $.get('/measurements', {
   }, function(data) {
   $("#temperature").text(data.temperature);
   $("#angle").text(data.angle);
   $("#x_rotation").text(data.x_rotation);
   $("#y_rotation").text(data.y_rotation);
   $("#gyro_temp").text(data.gyro_temp);
   $("#cpu_temp").text(data.cpu_temp);
   $("#temp_rc1").text(data.temp_rc1);
   $("#pitch_current").text(data.temp_rc1);
   $("#rotation_current").text(data.rotation_current);
   $("#errors_rc1").text(data.errors_rc1);
   $("#temp_rc2").text(data.temp_rc2);
   $("#column_current").text(data.column_current);
   $("#launch_current").text(data.launch_current);
   $("#errors_rc2").text(data.errors_rc2);
   $("#temp_rc3").text(data.temp_rc3);
   $("#case_open_current").text(data.case_open_current);
   $("#case_close_current").text(data.case_close_current);
   $("#errors_rc3").text(data.errors_rc3);
   
   });
}, 1000)
/*
setInterval(() => {
  $.get('/rc1_data', {
   }, function(data) {
   $("#temp_rc1").text(data.temp_rc1);
   $("#pitch_current").text(data.temp_rc1);
   $("#rotation_current").text(data.rotation_current);
   $("#errors_rc1").text(data.errors_rc1);
   });
   
}, 1000)

setInterval(() => {
  $.get('/rc2_data', {
   }, function(data) {
   $("#temp_rc2").text(data.temp_rc2);
   $("#column_current").text(data.column_current);
   $("#launch_current").text(data.launch_current);
   $("#errors_rc2").text(data.errors_rc2);
   });
   
}, 1000)


setInterval(() => {
  $.get('/rc3_data', {
   }, function(data) {
   $("#temp_rc3").text(data.temp_rc3);
   $("#case_open_current").text(data.case_open_current);
   $("#case_close_current").text(data.case_close_current);
   $("#errors_rc3").text(data.errors_rc3);
   
   });
}, 1000)

*/
  $('#script_data_out_temp').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_data_out_temp', {
   }, function(data) {
   $("#temp").text(data.temp);
   });
   return false;
  });


  $('#script_stop').on('mouseup touchend', function(event) {
    event.preventDefault();
    $.post('/app_stop');
   });
   
   $('#script_stop_all').on('mouseup touchend', function(event) {
    event.preventDefault();
    $.post('/app_stop');
   });


  $('#script_standby').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_standby', {
     standby: $('input[name="standby"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_prepare').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_prepare', {
     prepare: $('input[name="prepare"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_launch').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_launch', {
     launch: $('input[name="launch"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_mount').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_mount', {
     mount: $('input[name="mount"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });


  $('#script_automatic_launch').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_automatic_launch', {
     automatic_launch: $('input[name="automatic_launch"]').val()
   }).fail(function(response) {
     if (response.status === 403) {
       alert('Encoders are not ready');
     }
   });
   return false;
  });

  $('#script_change_pitch').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_change_pitch', {
     pitch_position_prepare: $('input[name="pitch_position_prepare"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between 0 and 90');
     }
   });
   return false;
  });

  $('#script_change_lift').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_change_lift', {
     lift_position_prepare: $('input[name="lift_position_prepare"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between 0 and 130');
     }
   });
   return false;
  });

  $('#script_change_rotation').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_change_rotation', {
     rotation_position_prepare: $('input[name="rotation_position_prepare"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between -180 and 180');
     }
   });
   return false;
  });

  $('#script_change_speed').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_change_speed', {
     speed: $('input[name="speed"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between 1 and 10');
     }
   });
   return false;
  });

  $('#script_change_acceleration').on('mouseup touchend', function(event) {
   event.preventDefault();
   $.post('/app_change_acceleration', {
     acceleration: $('input[name="acceleration"]').val()
   }).fail(function(response) {
     if (response.status === 400) {
       alert('Value should be between 1 and 48');
     }
   });
   return false;
  });

});


function show_manual() {
    var dat1 = document.getElementById("data_display");
    var man1 = document.getElementById("manual_pitch_buttons");
    var man2 = document.getElementById("manual_rotation_buttons");
    var man3 = document.getElementById("manual_lift_buttons");
    var man4 = document.getElementById("manual_launch_buttons");
    var man5 = document.getElementById("manual_buttons_down");
    var man6 = document.getElementById("manual_case_buttons");
    var aut1 = document.getElementById("automatic_position_buttons");
    var aut2 = document.getElementById("automatic_launch_buttons");
    var set1 = document.getElementById("settings_launch");
    man1.style.display = "flex";
    man2.style.display = "flex";
    man3.style.display = "flex";
    man4.style.display = "flex";
    man5.style.display = "flex";
    aut1.style.display = "none";
    aut2.style.display = "none";
    set1.style.display = "none";
    dat1.style.display = "none";
    man6.style.display = "flex"
}

function show_automatic() {
  var dat1 = document.getElementById("data_display");
  var man1 = document.getElementById("manual_pitch_buttons");
  var man2 = document.getElementById("manual_rotation_buttons");
  var man3 = document.getElementById("manual_lift_buttons");
  var man4 = document.getElementById("manual_launch_buttons");
  var man5 = document.getElementById("manual_buttons_down");
  var man6 = document.getElementById("manual_case_buttons");
  var aut1 = document.getElementById("automatic_position_buttons");
  var aut2 = document.getElementById("automatic_launch_buttons");
  var set1 = document.getElementById("settings_launch");
  man1.style.display = "none";
  man2.style.display = "none";
  man3.style.display = "none";
  man4.style.display = "none";
  man5.style.display = "none";
  aut1.style.display = "flex";
  aut2.style.display = "flex";
  set1.style.display = "none";
  dat1.style.display = "none";
  man6.style.display = "flex"
}

function show_settings() {
  var dat1 = document.getElementById("data_display");
  var man1 = document.getElementById("manual_pitch_buttons");
  var man2 = document.getElementById("manual_rotation_buttons");
  var man3 = document.getElementById("manual_lift_buttons");
  var man4 = document.getElementById("manual_launch_buttons");
  var man5 = document.getElementById("manual_buttons_down");
  var man6 = document.getElementById("manual_case_buttons");
  var aut1 = document.getElementById("automatic_position_buttons");
  var aut2 = document.getElementById("automatic_launch_buttons");
  var set1 = document.getElementById("settings_launch");
  man1.style.display = "none";
  man2.style.display = "none";
  man3.style.display = "none";
  man4.style.display = "none";
  man5.style.display = "none";
  aut1.style.display = "none";
  aut2.style.display = "none";
  set1.style.display = "flex";
  dat1.style.display = "none";
  man6.style.display = "none"
}

function hide_video() {
    var vid = document.getElementById("div_video");
    var show_butt = document.getElementById("show_video_button");
    vid.style.display = "none";
    show_butt.style.display = "block";
}

function show_video() {
    var vid = document.getElementById("div_video");
    var show_butt = document.getElementById("show_video_button");
    vid.style.display = "block";
    show_butt.style.display = "none";
}

function show_data() {
  var dat1 = document.getElementById("data_display");
  var man1 = document.getElementById("manual_pitch_buttons");
  var man2 = document.getElementById("manual_rotation_buttons");
  var man3 = document.getElementById("manual_lift_buttons");
  var man4 = document.getElementById("manual_launch_buttons");
  var man5 = document.getElementById("manual_buttons_down");
  var man6 = document.getElementById("manual_case_buttons");
  var aut1 = document.getElementById("automatic_position_buttons");
  var aut2 = document.getElementById("automatic_launch_buttons");
  var set1 = document.getElementById("settings_launch");
  man1.style.display = "none";
  man2.style.display = "none";
  man3.style.display = "none";
  man4.style.display = "none";
  man5.style.display = "none";
  aut1.style.display = "none";
  aut2.style.display = "none";
  set1.style.display = "none";
  dat1.style.display = "flex";
  man6.style.display = "none"
}
