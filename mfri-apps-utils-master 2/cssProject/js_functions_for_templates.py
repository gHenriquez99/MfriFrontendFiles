
#import json
#import base64
#import time
import datetime


def start_script():
    return u'<script type="text/javascript">var $submitcounter = 0;'
    
def end_script():
    return u'</script>'

def start_doc_ready():
    return u'$(document).ready(function() {\n'

def end_doc_ready():
    return u'});\n'


def CheckUncheckAll_FS_js(js_function_name="CheckUncheckAllFS", controller_name=u'CheckAll', class_name=u'check_box'):
    #lss/asset/category/16/assets
#    <script type="text/javascript">
    return '''
function %s ()
    {
      var CBCheckAll = document.getElementsByName("%s");		
      var CBCheckBoxes = document.getElementsByClassName("%s");

      var CurrentCheckAllState = CBCheckAll[0].checked;	

      CBCheckAll[0].checked != CBCheckAll[0].checked;

      if (CBCheckBoxes.length > 0)	
      {

        for (i = 0; i < CBCheckBoxes.length; i++)
        {
    	  CBCheckBoxes[i].checked = ! CurrentCheckAllState; // CBCheckAll[0].checked ;
        }	
      }
      else
      {	
        CBCheckBoxes.checked = ! CurrentCheckAllState; // CBCheckAll[0].checked ;
      }
    }
''' % (js_function_name, controller_name, class_name)
#</script>

def DisableInputOnsubmit_JS(js_function_name='disable_input_buttons', prereg_button_id='FormButton_PR', move_button_id='FormButton_M', del_button_id='FormButton_D'):
    return '''
function %s(event) {\n
   $submitcounter++;\n
   if ($submitcounter > 1)\n
   {\n
     //event.preventDefault();
     $("#%s").hide();\n
     $("#%s").hide();\n
     $("#%s").hide();\n
     $("#FormButton_Busy").show("fast");
     //$("#FormButton_PR").submit();
   }\n
   return true;\n
}
''' % (js_function_name, prereg_button_id, move_button_id, del_button_id)

def RegFormDisableInputOnsubmit_JS(js_function_name='disable_input_buttons', save_button_id='id_register', change_button_id='id_change', cancel_button_id='id_cancel'):
    return '''
function %s(event) {\n
   $submitcounter++;\n
   if ($submitcounter > 1)\n
   {\n
     $("#%s").val("Sending...");\n
     $("#%s").val("");\n
     $("#%s").val("");\n
     $(":input").attr("disabled", "disabled");\n
     $("a").click(function(e) { e.preventDefault(); });\n
     event.preventDefault();\n
   }\n
   return true;\n
}
''' % (js_function_name, save_button_id, change_button_id, cancel_button_id)

def open_new_window_js(url_for_new_window=None, window_name=u'_blank'):
    
    form_js = u''
    
    form_js += u'<script type="text/javascript">'
    form_js += u'window.open("%s","%s");' % (url_for_new_window, window_name)
    
    form_js += '</script>'
    
    return form_js
    

def JSDatePicker(field_id_name=None, Default_Value=datetime.datetime.now().strftime('%m-%d-%Y'), StartDate=None, StartYear=1930, EndDate=None, EndYear=str(int(datetime.datetime.now().strftime('%Y')) + 4), Date_format='mm-dd-yy'):

    if not field_id_name:
        return ''
        
    minDate = ''
    maxDate = ''

    if StartDate:
        if not StartYear:
            StartYear = StartDate.strftime('%Y')
        minDate = u',minDate: "%s"' % (StartDate.strftime('%m-%d-%Y'))

    if EndDate:
        if not EndYear:
            EndYear = EndDate.strftime('%Y')
        maxDate = u',maxDate: "%s"' % (EndDate.strftime('%m-%d-%Y'))

#    js_datepicker = u'<script type="text/javascript">$(document).ready(function() {$("#%s").datepicker({ changeMonth: true,changeYear: true, dateFormat : "%s", yearRange: "%s:%s", defaultDate: "%s"%s%s});});</script>' % (field_id_name,  Date_format, str(StartYear), str(EndYear), Default_Value, minDate, maxDate )
    #assert False
    return u'<script type="text/javascript">$(document).ready(function() {$("#%s").datepicker({ changeMonth: true,changeYear: true, dateFormat : "%s", yearRange: "%s:%s", defaultDate: "%s"%s%s});});</script>' % (field_id_name,  Date_format, str(StartYear), str(EndYear), Default_Value, minDate, maxDate )

def JSTimePicker(field_id_name=None, StartTime='00:00', EndTime='23:59'): #, Date_format='hh-mm' Default_Value=datetime.datetime.now().strftime('%H:%M'), 

    if not field_id_name:
        return ''

    return u'<script type="text/javascript">$(document).ready(function() {$("#%s").timePicker({startTime: "%s", endTime: "%s",show24Hours: true,separator: ":",step: 15});});</script>'  % (field_id_name, str(StartTime), str(EndTime) )

def JSOnChangeEvent(field_id_name=None, function_name=None, function_code=None): 

    if not field_id_name:
        return ''

    if not function_name:
        return ''

    js_section_start = u'<script type="text/javascript">$(document).ready(' #$(document).ready(

    js_section = u'function() {$("#%s").bind("change", function() { %s(); } );}' % (field_id_name, function_name)

    if function_code:
        js_section +=  u'function %s() {%s}' % (function_name, function_code) 
    
    js_secton_end = u');</script>' #);

    return u'%s%s%s'  % (js_section_start, js_section, js_secton_end )

def JSOnBlurEvent(field_id_name=None, function_name=None, function_code=None): 

    if not field_id_name:
        return ''

    if not function_name:
        return ''

    js_section_start = u'<script type="text/javascript">$(document).ready(' #$(document).ready(

    js_section = u'function() {$("#%s").bind("blur", function() { %s(); } );}' % (field_id_name, function_name)

    if function_code:
        js_section +=  u'function %s() {%s}' % (function_name, function_code) 
    
    js_secton_end = u');</script>' #);

    return u'%s%s%s'  % (js_section_start, js_section, js_secton_end )

def JSOnClickEvent(field_id_name=None, function_name=None, function_code=None): 

    if not field_id_name:
        return ''

    if not function_name:
        return ''

    js_section_start = u'<script type="text/javascript">$(document).ready(' #$(document).ready(

    js_section = u'function() {$("#%s").bind("click", function(event) { return %s(event); } );});' % (field_id_name, function_name) #);

    if function_code:
        js_section +=  u'function %s(event) {%s});' % (function_name, function_code) 
    
    js_secton_end = u'</script>' #);

    return u'%s%s%s'  % (js_section_start, js_section, js_secton_end )

def write_select_checkbox_js(checkbox_id=None):
    
    if not checkbox_id:
        return ''
    
    return '''
''' % (checkbox_id)

def write_unselect_checkbox_js(checkbox_id=None):
    
    if not checkbox_id:
        return ''
    
    return '''
''' % (checkbox_id)


def write_clear_list_js(checkbox_id=None, list_id=None, function_name='clear_list'):
    
    if not (checkbox_id or list_id):
        return u''
        
    return '''
function %s() {
    if ($("#%s:checked").val()?true:false)
    {
        $("#%s")[0].selectedIndex = -1;
    }
}
''' % (function_name, checkbox_id, list_id)

def write_clear_checkbox_js(checkbox_id=None, list_id=None, function_name='clear_checkbox'):
    
    if not (checkbox_id or list_id):
        return u''
        
    return '''
function %s() {\n
    if ($("#%s option:selected").val())
    {
        $("#%s").attr('checked', false);
    }
    else
    {
        $("#%s").attr('checked', true);
    }

}
''' % (function_name, list_id, checkbox_id, checkbox_id)



def change_class_js(function_name='register_button_update', object_id='id_register', new_class='btn btn-primary spinner-border spinner-border-sm' ):
    return '''\n
function %s() {\n
    $("#%s").attr("class", "%s");\n
}\n
''' % (function_name, object_id, new_class)


def InitialHideProgressSpinner_js(progress_spinner_id='id_progress_spinner'):
    
    hide_progress_spinner_js = u'$("#%s").hide();\n' % (progress_spinner_id) 
    return hide_progress_spinner_js + '\n' # + show_edit_form_js + '\n'

def HideFormButtonsShowProgressSpinner_js(on_click_button_id='id_cr', hide_button_id_list=('id_ut', 'id_cr'), progress_spinner_id='id_progress_spinner'):
    
    if not hide_button_id_list:
        hide_button_id_list.append(on_click_button_id)
    
    hide_js = u''
    
    for button_id in hide_button_id_list:
        hide_js += u'\n$("#%s").hide();' % (button_id)
    
    #bind_id_register_click_js = u'$("#%s").click(function(event){\n$("#%s").hide(); \n\n$("#%s").show("fast");\n});\n\n' % (register_button_id, register_button_id, progress_spinner_id) 
    bind_id_register_click_js = u'$("#%s").click(function(event){%s \n\n$("#%s").show("fast");\n});\n\n' % (on_click_button_id, hide_js, progress_spinner_id) 


   #if show_edit_form:
    #    show_edit_form_js = u'$("#%s").hide();\n$("#%s").show();\n' % (show_edit_form_button_id, edit_form_id)
    #else:
    #    show_edit_form_js = u'$("#%s").show();\n$("#%s").hide();\n' % (show_edit_form_button_id, edit_form_id)
    
    
    return bind_id_register_click_js + '\n' # + show_edit_form_js + '\n'



