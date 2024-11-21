import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import axios from 'axios';


function App() {
  const[aritcal, setArtical] = useState("");
  const[articalCategory, setArticalCategory] = useState("");
  const BASE_API = "http://127.0.0.1:5000"
  const [modelAcc, setModelAcc] = useState({
    cnn: "",
    lstm: "",
    lr: "",
    nb: "",
    svm: ""
    
  })

  const[showNews, setShowNews] = useState(false);
  const[newsType, setNewsType] = useState("")



  const handleSubmit = () => {
    const data = {
      artical : aritcal,
    }
    axios.post(BASE_API + "/predict", { "article": String(aritcal) }).then((resGemi) => {
      setNewsType(resGemi.data.NaiveBayes);
      setModelAcc({
        cnn: resGemi.data.CNN,
        lstm: resGemi.data.LSTM,
        lr: resGemi.data.LogisticRegression,
        nb: resGemi.data.NaiveBayes,
        svm: resGemi.data.SVM 
      })

      setShowNews(true)
      
    }).catch((error) => {
      console.error("Error during prediction:", error);
    });

  }

  const handleToggle = () => {
    setShowNews(false)
  }
 

  return (
    <div className="App">
      {
        showNews ? 
        (
        <div>
          <h1>
            {newsType == "Fake News" ? "👎 Opps! Looks Like it is Fake" : "👍 Yeyy This is True News"}
          </h1>
          <button className='submit-button' onClick={handleToggle}>Ok!</button>
        </div>
      ):
      (<div>
        <h1>Enter Your NEWS!</h1>
        <div className='main-Container'>  
          <div className='form-container'>
            <div className='input-container'>
              <textarea className='article-input' rows={15} placeholder='Enter your article' onChange={e => setArtical(e.target.value)}></textarea>
              <input className='article-input' placeholder='Enter your article Category' onChange={e => setArticalCategory(e.target.value)} ></input>
              <button className='submit-button' onClick={handleSubmit}>Submit</button>
            </div>
          </div>
        </div> </div>) 
      }
    </div>
  );
}

export default App;
