const rhymePost = document.querySelector('#rhyme_post')
const printRhyme = document.getElementById('print_rhyme')
rhymePost.addEventListener('submit', function(event){
    event.preventDefault()
    let word = this.children[0].value
    
    console.log(word)

    fetch(`https://api.datamuse.com/words?rel_nry=${word}&max=100`)
    .then(resp => resp.json())
    .then(data =>{
        printRhyme.innerHTML = null
        if(data.length < 1){
            printRhyme.innerHTML +=
        `
        There are no rhyming words at this time. Check spelling or 
        if your word is one syllable, I regret to inform 
        you, we do not supply rhymes for one syllable words. Be better.
        `
        }
        for(const obj of data){
            console.log(obj['word'])
            
            printRhyme.innerHTML +=
            `
            ${obj['word']} <br> 
            `
        }
    })
    .catch(err => console.log(err))
})

const dictPost = document.querySelector('#dict_post')
const printDict = document.getElementById('print_dict')
dictPost.addEventListener('submit', function(event){
    event.preventDefault()
    let word = this.children[0].value
    
    console.log(word)

    fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${word}`)
    .then(resp => resp.json())
    .then(data =>{
        printDict.innerHTML = null
        // console.log(data[0].meanings[0].definitions)
        
        for(const obj of data[0].meanings[0].definitions){
            console.log(obj.definition)
            printDict.innerHTML +=
            `
            Definition: ${obj['definition']} <br> <br>  
            `
        }
    })
    .catch(err => console.log(err))
})

// document.getElementById('rhyme_post').addEventListener(onkeydown, check())

// function check(e){
//     console.log(e.keycode)
//     if(e.keycode === 13){

//     }
// }



document.getElementById("r_btn").onclick = function(){
    document.getElementById("content").style.color = 'red';
}

document.getElementById("g_btn").onclick = function(){
    document.getElementById("content").style.color = 'green';
}

document.getElementById("b_btn").onclick = function(){
    document.getElementById("content").style.color = 'blue';
}

document.getElementById("bk_btn").onclick = function(){
    document.getElementById("content").style.color = 'black';
}

document.getElementById("p_btn").onclick = function(){
    document.getElementById("content").style.color = 'purple';
}

document.getElementById("o_btn").onclick = function(){
    document.getElementById("content").style.color = 'rgb(229, 154, 15)';
}