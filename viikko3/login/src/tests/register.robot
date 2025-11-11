*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  eetu
    Set Password  salainen123
    Set Password_confirmation  salainen123
    Click Button  Register
    Register Succeed

Register With Too Short Username And Valid Password
    Set Username  ee
    Set Password  salainen123
    Set Password_confirmation  salainen123
    Click Button  Register
    Register Should Fail With Message  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  eetu
    Set Password  salain
    Set Password_confirmation  salain
    Click Button  Register
    Register Should Fail With Message  Password must be at least 8 characters long

Register With Valid Username And Invalid Password
    set Username  eetu
    Set Password  salainen
    Set Password_confirmation  salainen
    Click Button  Register
    Register Should Fail With Message  Password must contain at least one non-letter character

Register With Nonmatching Password And Password Confirmation
    Set Username  eetu
    Set Password  salainen123
    Set Password_confirmation  salainen124
    Click Button  Register
    Register Should Fail With Message  Password and password confirmation do not match

Register With Username That Is Already In Use
    Set Username  pekka
    Set Password  pekka123
    Set Password_confirmation  pekka123
    Click Button  Register
    Register Should Fail With Message  Username is already taken

*** Keywords ***

Register Succeed
    Welcome Page Should Be Open

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}
Set username
    [Arguments]  ${username}
    Input Text  username  ${username}  

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  pekka  pekka123
    Go To  ${REGISTER_URL}
