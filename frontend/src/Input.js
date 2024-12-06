import { useState } from "react";

const url = "http://127.0.0.1:5000/feedback"

const Input = () => {

    const [feedback, setFeedback] = useState('');

    function handleChange(e) {
        setFeedback(e.target.value);
    }

    function handleClick() {
        console.log(feedback);
        const obj = {
            "feedback": feedback
        };
        fetch(url, {
            method: "POST",
            body: JSON.stringify(obj),
            headers: new Headers({'content-type': 'application/json'}),
        })
        setFeedback("");
    }
    
    return (
        <>
        <div>
            <p>Feedback: </p>
            <textarea id="feedbackarea" name="w3review" rows="4" cols="50" 
            value={feedback} onChange={handleChange}>
            </textarea>
        </div>
        <button onClick={handleClick}>Submit</button>
        </>
    )
}

export default Input;