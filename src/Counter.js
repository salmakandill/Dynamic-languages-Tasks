import { useState } from "react";
import './Counter.css'

function Counter(){
    const [count,setCount]=useState(0);
    return (
        <div  className="counter-box">
            <h2 className="counter-number"> Count : {count}</h2>
            <button className="counter-btn" onClick={()=>setCount(count+2)} >Increase by 2 </button>
            <br/> <br/>
            <button className="counter-btn" onClick={()=>setCount(count-1)} >Decrease by 1 </button>
        </div>
    );
}
export default Counter;