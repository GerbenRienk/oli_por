

def write_odm_line( oc_item_name, ls_item_value, is_date=False, is_time=False, is_decimal=False, is_integer=False, is_utf8 = False):
    _one_line = ''
    if (ls_item_value):
        _this_value = ls_item_value
        if (is_date):
            _this_value = ls_item_value[0:10]
        if (is_time):
            # time field: for now we do nothing with it
            _this_value = _this_value
            
        if (is_decimal):
            _this_value = str(ls_item_value)
        if (is_integer):
            _this_value = str(int(float(ls_item_value)))
        if (is_utf8):
            _this_value = str(_this_value.encode(encoding="ascii",errors="xmlcharrefreplace"))
            # now we have something like b'some text &amp; more' so we want to loose the first two characters and the last one
            # TODO: make this nicer somehow
            _this_value = _this_value[2:]
            _this_value = _this_value[:-1]
                   
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value="' + _this_value + '"/>'
    else:
        _one_line = _one_line + '            <ItemData ItemOID="' + oc_item_name + '" Value=""/>'
    #print(_one_line)
    return _one_line

def compose_odm(study_subject_oid, data_odk):
    """
    compose the xml-content to send to the web-service 
    just for this one occasion we write out everything literally
    and we make a big exception for birth-weight, which is given 
    in grams, but must be imported in kilo's and grams 
    """
    #print('in compose_odm ', study_subject_oid)
    if (data_odk['q5birthweightgram'] is not None):
        kilograms = int(float(data_odk['q5birthweightgram'])/1000)
        I_PTFAM_BIRTHWEIGHTKG = str(kilograms)
        grams = int(float(data_odk['q5birthweightgram']) - kilograms * 1000)
        I_PTFAM_BIRTHWEIGHTGR = str(grams)
        #print(data_odk['q5birthweightgram'], I_PTFAM_BIRTHWEIGHTKG, I_PTFAM_BIRTHWEIGHTGR)
    else:
        I_PTFAM_BIRTHWEIGHTKG = ''
        I_PTFAM_BIRTHWEIGHTGR = ''
    
    # opening tags
    _odm_data = ''
    _odm_data = _odm_data + '<ODM>'
    _odm_data = _odm_data + '  <ClinicalData StudyOID="S_CDPOR">'
    _odm_data = _odm_data + '    <SubjectData SubjectKey="' + study_subject_oid + '">'
    _odm_data = _odm_data + '      <StudyEventData StudyEventOID="SE_POR_CD">'
    _odm_data = _odm_data + '        <FormData FormOID="F_PTFAMILYFORM_V13">'
    _odm_data = _odm_data + '          <ItemGroupData ItemGroupOID="IG_PTFAM_UNGROUPED" ItemGroupRepeatKey="1" TransactionType="Insert">'
    # data
    _odm_data = _odm_data + write_odm_line('I_PTFAM_RELATIONSHIP', data_odk['q1relationship'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_RELATIONSHIPOTH', data_odk['q1relationshipother'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_DATEOFBIRTHCOMPLETE', data_odk['q3birthdatecomplete'], is_date=True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_GENDER', data_odk['q4sex'])
    # begin first exception !
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BIRTHWEIGHTKG', I_PTFAM_BIRTHWEIGHTKG)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BIRTHWEIGHTGR', I_PTFAM_BIRTHWEIGHTGR)
    # end first exception
    
    # generated from testcosi5
    _odm_data = _odm_data + write_odm_line('I_PTFAM_LATEEARLYBIRTH', data_odk['q6fullterm'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTFEDEVER_2', data_odk['q7breastfed'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTFEDHOWLONG', data_odk['q7breastfedmonths'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTEXCLEVER', data_odk['q8breastfedexclusive'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREASTEXCLUSIVE', data_odk['q8breastexclusive'], is_integer = True)   
    _odm_data = _odm_data + write_odm_line('I_PTFAM_DISTANCESCHOOLHOME', data_odk['q9distance'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_TRANSPSCHOOLFROM', data_odk['q10transpschoolfrom'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_TRANSPSCHOOLTO', data_odk['q10transpschoolto'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_REASONMOTORIZED', data_odk['q10areasonmotorized']) 
    _odm_data = _odm_data + write_odm_line('I_PTFAM_REASONMOTORIZEDOTH', data_odk['q10areasonmotorizedo'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SAFEROUTESCHOOL', data_odk['q11routesafe']) 
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPORTCLUB_2', data_odk['q12sportclubs'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPORTCLUBFREQ', data_odk['q13sportclubsfrequen'])
    
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BEDTIME', data_odk['q14bedtime'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WAKEUPTIME', data_odk['q15wakeuptime'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDSPLAYINGACTIVE', data_odk['q16playoutweekdays'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEPLAYINGACTIVE', data_odk['q16playouteweekdays'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDREADING', data_odk['q17readingweekdays'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEREADING', data_odk['q17readingweekends'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDELECTRONICSH', data_odk['q18wdelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDELECTRONICSM', data_odk['q18wdelectronicsm'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEELECTRONICSH', data_odk['q18weelectronicsh'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEELECTRONICSM', data_odk['q18weelectronicsm'], is_integer = True)
    
    # begin second exception !
    # these checkboxes can only be Y in ls
    # which corresponds to 1 in oc
    if (data_odk['q18wdelectrnotatall[NAA]'] == 'Y'):
        q18wdelectrnotatall = '1'
    else:
        q18wdelectrnotatall = ''
    if (data_odk['q18weelectrnotatall[NAA]'] == 'Y'):
        q18weelectrnotatall = '1'
    else:
        q18weelectrnotatall = ''
        
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WDELECTRNOTATALL', q18wdelectrnotatall)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEELECTRNOTATALL', q18weelectrnotatall)
    # end second exception !
    
    _odm_data = _odm_data + write_odm_line('I_PTFAM_BREAKFAST', data_odk['q19breakfast'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCANDY', data_odk['q20[Candy]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCEREALS', data_odk['q20[Cereals]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_CEREALSSUGAR_2', data_odk['q20cerealssugar'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCHEESE', data_odk['q20[Cheese]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQCHIPS', data_odk['q20[Chips]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQDAIRY', data_odk['q20[Dairy]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQDIET', data_odk['q20[DietSoftDrinks]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQEGG', data_odk['q20[Egg]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFISH', data_odk['q20[Fish]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFLAVOUREDMILK', data_odk['q20[FlavouredMilk]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFRUIT', data_odk['q20[FreshFruit]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQFRUITJUICE', data_odk['q20[FruitJuice]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQLEGUMES', data_odk['q20[Legumes]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQLOWFATMILK', data_odk['q20[LowFatMilk]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQMEAT', data_odk['q20[Meat]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQSOFTDRINKS', data_odk['q20[SoftDrinksSugar]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQVEGETABLES', data_odk['q20[Vegetables]'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_FREQWHOLEFATMILK', data_odk['q20[WholeFatMilk]'])
    
    _odm_data = _odm_data + write_odm_line('I_PTFAM_WEIGHTOPINION', data_odk['q21weightopinion'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOUSEHOLDBLOODPRESSURE', data_odk['q22househouldbloodpr'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOUSEHOLDDIABETES', data_odk['q23householddiabetes'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HOUSEHOLDCHOLESTEROL', data_odk['q24householdcholeste'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPOUSEAGE', data_odk['q25spousesage'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPOUSEHEIGHT', data_odk['q25spouseheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_SPOUSEWEIGHT', data_odk['q25spouseweight'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_YOUAGE', data_odk['q25youage'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_YOUHEIGHT', data_odk['q25youheight'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_YOUWEIGHT', data_odk['q25youweight'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRBROTHER', data_odk['q26hmnr[Brother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRELSE', data_odk['q26hmnr[Else]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRELSESPEC', data_odk['q26hmnrelsespec'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRFATHER', data_odk['q26hmnr[Father]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRFOSTER', data_odk['q26hmnr[Foster]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRGRANDFATHER', data_odk['q26hmnr[Grandfathers]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRGRANDMOTHER', data_odk['q26hmnr[Grandmothers]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRMOTHER', data_odk['q26hmnr[Mother]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRSISTER', data_odk['q26hmnr[Sister]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRSTEPFATHER', data_odk['q26hmnr[Stepfather]'], is_integer = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_HMNRSTEPMOTHER', data_odk['q26hmnr[Stepmother]'], is_integer = True)
    
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_CHILDBORNOTH_2', data_odk['q27childbornoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_CHILDBORN_2', data_odk['q27childborn'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_MOTHERBORNOTH_2', data_odk['q28motherbornoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_MOTHERBORN_2', data_odk['q28motherborn'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_FATHERBORNOTH_2', data_odk['q29fatherbornoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_FATHERBORN_2', data_odk['q29fatherborn'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_LANGUAGEOTH', data_odk['q30languageoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_PT_LANGUAGE', data_odk['q30language'])
    
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EDUSPOUSE_2', data_odk['q31eduspouse'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EDUYOU', data_odk['q31eduyou'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_EARNINGS', data_odk['q32earnings'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSE_2', data_odk['q33occupspouse'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPSPOUSEOTH', data_odk['q33occupspouseoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOU', data_odk['q33occupyou'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_OCCUPYOUOTH', data_odk['q33occupyouoth'], is_utf8 = True)
    _odm_data = _odm_data + write_odm_line('I_PTFAM_DATECOMPLETION', data_odk['q34datecompletion'])
    _odm_data = _odm_data + write_odm_line('I_PTFAM_REMARKS', data_odk['q35remarks'], is_utf8 = True)




    # closing tags
    _odm_data = _odm_data + '          </ItemGroupData>'
    _odm_data = _odm_data + '        </FormData>'
    _odm_data = _odm_data + '      </StudyEventData>'
    _odm_data = _odm_data + '    </SubjectData>'
    _odm_data = _odm_data + '  </ClinicalData>'
    _odm_data = _odm_data + '</ODM>'

    return _odm_data
