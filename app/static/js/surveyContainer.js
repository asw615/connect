Survey.StylesManager.applyTheme("modern");

var surveyJSON = {"logoPosition":"right","pages":[{"name":"page1","elements":[{"type":"text","name":"question1","title":"Hvad hedder du?","isRequired":true}]},{"name":"page2","elements":[{"type":"multipletext","name":"question2","title":"Hvem arbejder du bedst sammen med i klassen?","items":[{"name":"text1","title":"1."},{"name":"2."}]}]}]};

function sendDataToServer(survey) {
    //send Ajax request to your web server
    alert("The results are: " + JSON.stringify(survey.data));
}

var survey = new Survey.Model(surveyJSON);
$("#surveyContainer").SurveyWindow({
    model: survey,
    onComplete: sendDataToServer
});
