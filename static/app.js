let gameId = null
let state = null
// armazenar soluções completas retornadas pelo servidor (objeto com path, visited, time_ms)
let persistedSolutions = { bfs: null, dfs: null }
// algoritmo atualmente exibido: 'bfs' | 'dfs' | null
let displaySelected = null
// disponibilidade do jump scare (imagem/áudio)
let jumpscareAvailable = { img: false, audio: false }
const canvas = document.getElementById('maze')
const ctx = canvas.getContext('2d')

document.getElementById('newBtn').addEventListener('click', createNew)
document.getElementById('bfsBtn').addEventListener('click', () => solve('bfs'))
document.getElementById('dfsBtn').addEventListener('click', () => solve('dfs'))

// pré-carrega e testa mídia do jump scare (se houver)
;(function preloadJumpscare(){
  const img = new Image()
  img.src = '/static/media/susto.jpg'
  img.onload = () => { jumpscareAvailable.img = true }
  img.onerror = () => { jumpscareAvailable.img = false }

  const a = document.createElement('audio')
  a.src = '/static/media/grito.wav'
  a.preload = 'auto'
  a.addEventListener('canplaythrough', () => { jumpscareAvailable.audio = true })
  a.addEventListener('error', () => { jumpscareAvailable.audio = false })
  // append to DOM so browser may fetch it (hidden)
  a.style.display = 'none'
  a.id = '__preload_jump_audio'
  document.body.appendChild(a)
})()

window.addEventListener('keydown', (e) => {
  if (!gameId) return
  const mapping = {ArrowUp: 'up', ArrowRight: 'right', ArrowDown: 'down', ArrowLeft: 'left'}
  if (mapping[e.key]) {
    fetch('/api/move', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({game_id: gameId, direction: mapping[e.key]})
    }).then(r => r.json()).then(j => {
      state = j.state
      // sincronizar soluções completas se o servidor as possui
      if (state && state.solutions) {
        persistedSolutions.bfs = state.solutions.bfs || persistedSolutions.bfs
        persistedSolutions.dfs = state.solutions.dfs || persistedSolutions.dfs
      }
      // mover não altera qual solução está sendo exibida
      draw()
      document.getElementById('status').innerText = j.moved ? 'Movido' : 'Movimento bloqueado'
    })
  }
})

function createNew(){
  const cols = parseInt(document.getElementById('cols').value || 20)
  const rows = parseInt(document.getElementById('rows').value || 15)
  fetch('/api/new', {method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({cols, rows})})
    .then(r => r.json()).then(j => {
      gameId = j.game_id
      state = j.state
      // limpar soluções persistidas
      persistedSolutions = { bfs: null, dfs: null }
      displaySelected = null
      // se o servidor retornou soluções armazenadas, populá-las
      if (state && state.solutions) {
        if (state.solutions.bfs) persistedSolutions.bfs = state.solutions.bfs
        if (state.solutions.dfs) persistedSolutions.dfs = state.solutions.dfs
      }
      draw()
      document.getElementById('status').innerText = 'Novo jogo criado'
      document.getElementById('bfsStats').innerText = state && state.solutions && state.solutions.bfs ? `BFS: tempo ${state.solutions.bfs.time_ms.toFixed(2)} ms | passos ${state.solutions.bfs.path.length}` : 'BFS: —'
      document.getElementById('dfsStats').innerText = state && state.solutions && state.solutions.dfs ? `DFS: tempo ${state.solutions.dfs.time_ms.toFixed(2)} ms | passos ${state.solutions.dfs.path.length}` : 'DFS: —'
    })
}


function solve(alg){
  if (!gameId) return
  // se já calculamos essa solução, apenas exibi-la sem pedir novamente ao servidor
  if (persistedSolutions[alg]){
    displaySelected = alg
    const res = persistedSolutions[alg]
    document.getElementById('status').innerText = `Alg: ${alg.toUpperCase()} | tempo: ${res.time_ms.toFixed(2)} ms | passos: ${res.path.length}`
    if (alg === 'bfs') document.getElementById('bfsStats').innerText = `BFS: tempo ${res.time_ms.toFixed(2)} ms | passos: ${res.path.length}`
    if (alg === 'dfs') document.getElementById('dfsStats').innerText = `DFS: tempo ${res.time_ms.toFixed(2)} ms | passos: ${res.path.length}`
    draw()
    return
  }

  fetch('/api/solve', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({game_id: gameId, algorithm: alg})})
    .then(r => r.json()).then(j => {
      // API agora retorna { result: {...}, state: {...} }
      const res = j.result || j
      // armazenar solução completa localmente
      persistedSolutions[alg] = res
      // sincronizar estado do servidor
      if (j.state) state = j.state
      displaySelected = alg
      draw()
      document.getElementById('status').innerText = `Alg: ${alg.toUpperCase()} | tempo: ${res.time_ms.toFixed(2)} ms | passos: ${res.path.length}`
      // preencher stats
      if (alg === 'bfs') document.getElementById('bfsStats').innerText = `BFS: tempo ${res.time_ms.toFixed(2)} ms | passos: ${res.path.length}`
      if (alg === 'dfs') document.getElementById('dfsStats').innerText = `DFS: tempo ${res.time_ms.toFixed(2)} ms | passos: ${res.path.length}`
    })
}

function draw(){
  if (!state) return
  const cols = state.cols, rows = state.rows
  const cellW = Math.floor(canvas.width / cols)
  const cellH = Math.floor(canvas.height / rows)
  ctx.fillStyle = '#14141e'
  ctx.fillRect(0,0,canvas.width,canvas.height)

  for(let x=0;x<cols;x++){
    for(let y=0;y<rows;y++){
      const c = state.grid[x][y]
      const px = x*cellW, py = y*cellH
      ctx.strokeStyle = '#646478'
      ctx.lineWidth = 2
      // paredes: [top, right, bottom, left]
      if (c.paredes[0]) { ctx.beginPath(); ctx.moveTo(px,py); ctx.lineTo(px+cellW,py); ctx.stroke() }
      if (c.paredes[1]) { ctx.beginPath(); ctx.moveTo(px+cellW,py); ctx.lineTo(px+cellW,py+cellH); ctx.stroke() }
      if (c.paredes[2]) { ctx.beginPath(); ctx.moveTo(px+cellW,py+cellH); ctx.lineTo(px,py+cellH); ctx.stroke() }
      if (c.paredes[3]) { ctx.beginPath(); ctx.moveTo(px,py+cellH); ctx.lineTo(px,py); ctx.stroke() }
    }
  }
  // inicio
  ctx.fillStyle = '#00ff00'
  ctx.fillRect(state.inicio.x*cellW+4, state.inicio.y*cellH+4, cellW-8, cellH-8)
  // fim
  ctx.fillStyle = '#ff0000'
  ctx.fillRect(state.fim.x*cellW+4, state.fim.y*cellH+4, cellW-8, cellH-8)
  // jogador
  ctx.fillStyle = '#ffd700'
  ctx.fillRect(state.jogador.x*cellW+6, state.jogador.y*cellH+6, cellW-12, cellH-12)

  // desenhar células visitadas (área explorada) do algoritmo selecionado
  // cores inspiradas no cliente Pygame: BFS -> cinza claro, DFS -> violeta claro
  if (displaySelected === 'bfs' && persistedSolutions.bfs && persistedSolutions.bfs.visited) {
    ctx.fillStyle = 'rgba(45,45,60,0.65)'
    for (const v of persistedSolutions.bfs.visited) {
      ctx.fillRect(v.x*cellW+2, v.y*cellH+2, cellW-4, cellH-4)
    }
  }
  if (displaySelected === 'dfs' && persistedSolutions.dfs && persistedSolutions.dfs.visited) {
    ctx.fillStyle = 'rgba(55,45,70,0.65)'
    for (const v of persistedSolutions.dfs.visited) {
      ctx.fillRect(v.x*cellW+2, v.y*cellH+2, cellW-4, cellH-4)
    }
  }

  // desenhar apenas a solução atualmente selecionada (linha)
  if (displaySelected === 'bfs' && persistedSolutions.bfs && persistedSolutions.bfs.path) drawSolution(persistedSolutions.bfs.path, '#3388ff')
  if (displaySelected === 'dfs' && persistedSolutions.dfs && persistedSolutions.dfs.path) drawSolution(persistedSolutions.dfs.path, '#ff8c00')

  // mostrar jump scare se fim de jogo
  if (state.fim_de_jogo) triggerJumpScare()
}

function drawSolution(path, color='#3388ff'){
  if (!state || !path) return
  const cols = state.cols, rows = state.rows
  const cellW = Math.floor(canvas.width / cols)
  const cellH = Math.floor(canvas.height / rows)
  ctx.strokeStyle = color
  ctx.lineWidth = 4
  ctx.beginPath()
  for(let i=0;i<path.length;i++){
    const p = path[i]
    const cx = p.x*cellW + cellW/2
    const cy = p.y*cellH + cellH/2
    if (i===0) ctx.moveTo(cx,cy)
    else ctx.lineTo(cx,cy)
  }
  ctx.stroke()
}

function triggerJumpScare(){
  const overlay = document.getElementById('jumpscare')
  const img = document.getElementById('jumpscareImg')
  const audio = document.getElementById('jumpscareAudio')
  if (!overlay) return
  // mostrar overlay
  overlay.style.display = 'flex'
  // imagem somente se disponível
  if (!jumpscareAvailable.img && img) img.style.display = 'none'
  else if (img) img.style.display = 'block'
  // tocar audio se disponível
  if (jumpscareAvailable.audio && audio) {
    try {
      audio.currentTime = 0
      const p = audio.play()
      if (p && p.catch) p.catch(()=>{})
    } catch (e) {
      // falhar silenciosamente
    }
  }
}

// auto-create on load
createNew()
