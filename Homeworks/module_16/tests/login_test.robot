*** Settings ***
Documentation   A test suite that contains:
...                 - Login test
...                 - Adding a product to a cart test
Library         SeleniumLibrary
Library         ../libraries/MyLibrary.py
Variables       ../libraries/variables.py

*** Variables ***
${name_index}      2
${price_index}     3
&{monitor_test_data}        name=Apple monitor 24      price=400

*** Test Cases ***
Check Login Test
    [Documentation]     This test checks that a user can log in
    [Setup]             Open Browser To Main Page   ${URL}  ${BROWSER}
    Open Login Page
    Login User      ${USERNAME}     ${PASSWORD}
    Wait Until Page Contains Element     id = logout2
    Wait Until Element Contains     id = nameofuser     Welcome ${USERNAME}       5
    [Teardown]          Close Browser

Check Product Is Added To Cart Test
    [Documentation]     This test checks that a user can add a product to cart
    [Setup]             Open Browser And Login User   ${URL}  ${BROWSER}        ${USERNAME}     ${PASSWORD}

    Open Monitors Category
    ${sorted_products}=     MyLibrary.Sort Products Desc

    MyLibrary.Open Product Page     ${sorted_products}[0]
    Check Monitor Data On Product Page      ${monitor_test_data}
    Add Product To Cart

    Open Cart
    Check Monitor Data In Cart      ${monitor_test_data}        ${name_index}       ${price_index}

    [Teardown]          Close Browser


*** Keywords ***

Open Browser And Login User
    [Arguments]     ${URL}      ${BROWSER}      ${USERNAME}     ${PASSWORD}
    Open Browser To Main Page       ${URL}      ${BROWSER}
    Open Login Page
    Login User      ${USERNAME}     ${PASSWORD}
    Sleep       1s

Open Browser To Main Page
    [Arguments]     ${URL}  ${BROWSER}
    Open Browser    ${URL}  ${BROWSER}

Open Login Page
    Click Element                   id = login2
    Wait Until Page Contains Element     id = loginusername     5
    Wait Until Page Contains Element     id = loginpassword     5

Login User
    [Arguments]     ${USERNAME}     ${PASSWORD}
    Input Username      ${USERNAME}
    Input Password      ${PASSWORD}

    Click Element                   xpath=//button[text()="Log in"]

Input Username
    [Arguments]     ${USERNAME}
    # somehow awaits in Open Login Page don't work and no text is being input without explicit sleep
    # I've also tried some other awaits with no success
    Sleep       1s
    Input Text      id = loginusername  ${USERNAME}

Input Password
    [Arguments]     ${PASSWORD}
    Sleep       1s
    SeleniumLibrary.Input Password      id = loginpassword      ${PASSWORD}

Open Monitors Category
    [Tags]      ${SCREENSHOT_TAG}
    Click Element       xpath=//a[text()='Monitors']
    Sleep       1s

Add Product To Cart
    Click Element    css = a[onclick='addToCart(10)']
    Alert Should Be Present

Open Cart
    [Tags]      ${SCREENSHOT_TAG}
    Click Element    id = cartur

Get Cart Products
    [Return]     Get WebElements xpath = //*[@class='success'].//td

Check Monitor Data On Product Page
    [Arguments]     ${monitor_test_data}
    Wait Until Element Contains     xpath=//*[@class='name']        ${monitor_test_data}[name]
    Wait Until Element Contains     xpath=//*[@class='price-container']       ${monitor_test_data}[price]

Check Monitor Data In Cart
    [Arguments]     ${monitor_test_data}        ${name_index}      ${price_index}
    Wait Until Element Contains     xpath=//*[@class='success']//td[${name_index}]      ${monitor_test_data}[name]
    Wait Until Element Contains     xpath=//*[@class='success']//td[${price_index}]      ${monitor_test_data}[price]