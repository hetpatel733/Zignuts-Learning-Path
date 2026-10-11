// main.js - handles fetching tasks and UI interactions

function getAuthHeaders() {
  const token = localStorage.getItem('access_token');
  return {
    'Content-Type': 'application/json',
    'Authorization': token ? `Bearer ${token}` : ''
  };
}

async function fetchTasks(params = {}) {
  const query = new URLSearchParams(params).toString();
  const url = `/api/tasks/${query ? '?' + query : ''}`;
  const resp = await fetch(url, {headers: getAuthHeaders()});
  if (resp.status === 401) {
    // Not authenticated – redirect to login page
    window.location.href = '/login/';
    return; // stop further processing
  }
  if (!resp.ok) {
    throw new Error('Failed to fetch tasks');
  }
  return await resp.json();
}

function renderTask(task) {
  const col = document.createElement('div');
  col.className = 'col-12 col-md-6 col-lg-4 mb-4';
  
  const isCompleted = task.status === 'Completed';
  const priorityBadgeClass = 
    task.priority === 'High' ? 'bg-danger' : 
    task.priority === 'Medium' ? 'bg-warning text-dark' : 'bg-info text-dark';
  const statusBadgeClass = isCompleted ? 'bg-success' : 'bg-secondary';

  col.innerHTML = `
    <div class="card h-100 shadow-sm border-0 task-card ${isCompleted ? 'opacity-75 bg-light' : 'bg-white'}" data-id="${task.id}">
      <div class="card-body d-flex flex-column">
        <div class="d-flex justify-content-between align-items-start mb-2">
          <span class="badge ${priorityBadgeClass} rounded-pill">${task.priority} Priority</span>
          <span class="badge ${statusBadgeClass} rounded-pill">${task.status}</span>
        </div>
        <h5 class="card-title fw-bold ${isCompleted ? 'text-decoration-line-through text-muted' : 'text-dark'}">${task.title}</h5>
        <p class="card-text text-muted flex-grow-1 small">${task.description || '<em>No description provided</em>'}</p>
        <div class="text-secondary small mb-3">
          <i class="bi bi-calendar3 me-1"></i> Due: <strong>${task.due_date}</strong>
        </div>
        <div class="d-flex gap-2 pt-2 border-top">
          ${!isCompleted ? `<button class="btn btn-sm btn-outline-success flex-grow-1 d-flex align-items-center justify-content-center gap-1" data-action="complete"><i class="bi bi-check2"></i> Complete</button>` : ''}
          <button class="btn btn-sm btn-outline-danger ${isCompleted ? 'w-100' : ''} d-flex align-items-center justify-content-center gap-1" data-action="delete"><i class="bi bi-trash"></i> Delete</button>
        </div>
      </div>
    </div>`;
  return col;
}

async function loadAndRender() {
  const statusEl = document.getElementById('status-filter');
  const priorityEl = document.getElementById('priority-filter');
  const searchEl = document.getElementById('search-input');
  const list = document.getElementById('task-list');

  if (!list) return;

  const params = {};
  if (statusEl && statusEl.value) params.status = statusEl.value;
  if (priorityEl && priorityEl.value) params.priority = priorityEl.value;
  if (searchEl && searchEl.value) params.search = searchEl.value;
  params.ordering = 'due_date';

  try {
    const tasks = await fetchTasks(params);
    if (!tasks) return; // redirected or unauthenticated
    list.innerHTML = '';
    if (tasks.length === 0) {
      list.innerHTML = `
        <div class="col-12 text-center py-5">
          <div class="text-muted mb-3"><i class="bi bi-inbox fs-1"></i></div>
          <h5 class="text-secondary">No tasks found</h5>
          <p class="text-muted small">Create your first task or change your filter options above.</p>
        </div>`;
      return;
    }
    tasks.forEach(t => list.appendChild(renderTask(t)));
  } catch (e) {
    console.error(e);
  }
}

// Create task handler (only on dashboard)
const taskCreateForm = document.getElementById('task-create-form');
if (taskCreateForm) {
  taskCreateForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = {
      title: form.title.value,
      description: form.description.value,
      due_date: form.due_date.value,
      priority: form.priority.value,
      status: 'Pending'
    };
    try {
      const resp = await fetch('/api/tasks/', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(data)
      });
      if (resp.ok) {
        form.reset();
        // Collapse create task form if bootstrap collapse instance exists
        const collapseEl = document.getElementById('createTaskForm');
        if (collapseEl && window.bootstrap) {
          const bsCollapse = bootstrap.Collapse.getInstance(collapseEl) || new bootstrap.Collapse(collapseEl, { toggle: false });
          bsCollapse.hide();
        }
        loadAndRender();
      } else if (resp.status === 401) {
        window.location.href = '/login/';
      } else {
        const err = await resp.json();
        alert('Error creating task: ' + JSON.stringify(err));
      }
    } catch (err) {
      alert('Network or server error creating task: ' + err.message);
    }
  });
}

// Delegated actions for task list (delete, complete) – only if task list exists
const taskList = document.getElementById('task-list');
if (taskList) {
  taskList.addEventListener('click', async function(e) {
    const btn = e.target;
    const action = btn.getAttribute('data-action');
    if (!action) return;
    const card = btn.closest('.task-card');
    const taskId = card.dataset.id;
    if (action === 'delete') {
      if (!confirm('Delete this task?')) return;
      const resp = await fetch(`/api/tasks/${taskId}/`, {method: 'DELETE', headers: getAuthHeaders()});
      if (resp.ok) loadAndRender();
    } else if (action === 'complete') {
      const resp = await fetch(`/api/tasks/${taskId}/`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify({status: 'Completed'})
      });
      if (resp.ok) loadAndRender();
    }
  });
}

// Apply filters button – only if present
const applyFiltersBtn = document.getElementById('apply-filters');
if (applyFiltersBtn) {
  applyFiltersBtn.addEventListener('click', loadAndRender);
}

// Initial load
loadAndRender();
