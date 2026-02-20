const pupilL = document.getElementById('pupil-left')
const pupilR = document.getElementById('pupil-right')
const eyeL = document.getElementById('eye-left')
const eyeR = document.getElementById('eye-right')
const face = document.getElementById('face')
const log = document.getElementById('log')
const promptInput = document.getElementById('prompt')
const sendBtn = document.getElementById('send')

function clamp(v, a, b){ return Math.max(a, Math.min(b, v)) }

function movePupil(eye, pupil, targetX, targetY){
  const rect = eye.getBoundingClientRect()
  const cx = rect.left + rect.width/2
  const cy = rect.top + rect.height/2
  const dx = targetX - cx
  const dy = targetY - cy
  const max = rect.width*0.18
  const dist = Math.sqrt(dx*dx + dy*dy)
  const r = Math.min(max, dist)
  const nx = (dx / (dist||1)) * r
  const ny = (dy / (dist||1)) * r
  pupil.style.transform = `translate(${nx}px, ${ny}px)`
}

document.addEventListener('mousemove', (e)=>{
  movePupil(eyeL, pupilL, e.clientX, e.clientY)
  movePupil(eyeR, pupilR, e.clientX, e.clientY)
})

function appendLog(who, text){
  const el = document.createElement('div')
  el.className = 'entry'
  el.innerHTML = `<strong>${who}:</strong> ${text}`
  log.appendChild(el)
  log.scrollTop = log.scrollHeight
}

async function sendPrompt(){
  const prompt = promptInput.value.trim()
  if(!prompt) return
  appendLog('You', prompt)
  promptInput.value = ''
  // blink and look forward
  pupilL.style.transform = 'translate(0,0) scale(0.9)'
  pupilR.style.transform = 'translate(0,0) scale(0.9)'
  appendLog('LetLet', '...thinking...')

  try{
    const res = await fetch('/api/chat', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({prompt})})
    const j = await res.json()
    if(j.error){
      appendLog('Error', j.error)
    } else {
      // replace last thinking entry
      const entries = log.getElementsByClassName('entry')
      if(entries.length) entries[entries.length-1].innerHTML = `<strong>LetLet:</strong> ${j.reply}`
      else appendLog('LetLet', j.reply)
    }
  }catch(err){
    appendLog('Error', err.message)
  }
}

sendBtn.addEventListener('click', sendPrompt)
promptInput.addEventListener('keydown',(e)=>{ if(e.key==='Enter') sendPrompt() })
