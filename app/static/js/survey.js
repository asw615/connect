const surveyForm = document.getElementById('survey-form');
      
        surveyForm.addEventListener('submit', function (event) {
          event.preventDefault();
      
          const classValue = document.getElementById('class-input').value;
          const nameValue = document.getElementById('name-input').value;
          const workValue = document.getElementById('work-input').value;
          const notWorkValue = document.getElementById('not-work-input').value;
      
          console.log('classValue:', classValue);
          console.log('nameValue:', nameValue);
      
          const surveyData = {
            class: classValue,
            name: nameValue,
            work: workValue,
            notWork: notWorkValue,
          };
      
          const surveyDataJson = JSON.stringify(surveyData);
      
          let folderName = `/data/${classValue}_${nameValue}.json`;
      
          console.log('folderName:', folderName);
      
          if (typeof localStorage !== 'undefined') {
            localStorage.setItem(folderName, surveyDataJson);
            const savedData = localStorage.getItem(folderName);
            console.log('savedData:', savedData);
      
            // Get the latest created file
            const latestFile = folderName;
      
            // Get the JSON data for the latest file
            const jsonData = surveyDataJson;
      
            // Convert JSON data to a blob
            const blob = new Blob([jsonData], { type: 'application/json' });
      
            // Create a URL with the blob
            const url = URL.createObjectURL(blob);
      
            // Create a link with the URL and click it to download the file
            const link = document.createElement('a');
            link.href = url;
            link.download = latestFile;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          } else {
            console.error('localStorage is not available in this browser');
          }
        });