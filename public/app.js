const state = {
  title: '',
  description: '',
  endpoints: [],
};

let endpointCounter = 1;

const endpointsContainer = document.getElementById('endpoints');
const endpointTemplate = document.getElementById('endpoint-template');
const headerRowTemplate = document.getElementById('header-row-template');
const parameterRowTemplate = document.getElementById('row-template');
const markdownPreview = document.getElementById('markdown-preview');
const importButton = document.getElementById('import-openapi');
const importInput = document.getElementById('import-file');

const titleInput = document.getElementById('doc-title');
const descriptionInput = document.getElementById('doc-description');

function createEndpoint() {
  return {
    id: `endpoint-${endpointCounter++}`,
    name: '',
    method: 'GET',
    path: '',
    summary: '',
    headers: [],
    parameters: [],
    requestExample: '',
    responseExample: '',
  };
}

function renderEndpoints() {
  endpointsContainer.innerHTML = '';
  state.endpoints.forEach((endpoint) => {
    const node = endpointTemplate.content.cloneNode(true).firstElementChild;
    node.dataset.id = endpoint.id;

    bindEndpointFields(node, endpoint);
    renderHeaderRows(node, endpoint);
    renderParameterRows(node, endpoint);
    endpointsContainer.appendChild(node);
  });
}

function bindEndpointFields(node, endpoint) {
  const topLevelFields = node.querySelectorAll('[data-field]');
  topLevelFields.forEach((el) => {
    const field = el.dataset.field;
    if (field === 'method') {
      el.value = endpoint.method;
      el.addEventListener('change', (event) => {
        endpoint.method = event.target.value;
        updatePreview();
      });
    } else if (field === 'requestExample' || field === 'responseExample' || field === 'summary') {
      el.value = endpoint[field];
      el.addEventListener('input', (event) => {
        endpoint[field] = event.target.value;
        updatePreview();
      });
    } else if (field === 'name' || field === 'path') {
      el.value = endpoint[field];
      el.addEventListener('input', (event) => {
        endpoint[field] = event.target.value;
        updatePreview();
      });
    }
  });

  node.querySelector('.remove-endpoint').addEventListener('click', () => {
    state.endpoints = state.endpoints.filter((item) => item.id !== endpoint.id);
    renderEndpoints();
    updatePreview();
  });

  node.querySelector('.add-header').addEventListener('click', () => {
    endpoint.headers.push({ name: '', value: '', description: '' });
    renderEndpoints();
    updatePreview();
  });

  node.querySelector('.add-parameter').addEventListener('click', () => {
    endpoint.parameters.push({ name: '', type: '', required: 'yes', description: '' });
    renderEndpoints();
    updatePreview();
  });
}

function renderHeaderRows(node, endpoint) {
  const container = node.querySelector('[data-collection="headers"]');
  container.innerHTML = '';
  endpoint.headers.forEach((header, index) => {
    const row = headerRowTemplate.content.cloneNode(true).firstElementChild;
    row.querySelector('[data-field="name"]').value = header.name;
    row.querySelector('[data-field="value"]').value = header.value;
    row.querySelector('[data-field="description"]').value = header.description;

    row.querySelectorAll('[data-field]').forEach((input) => {
      input.addEventListener('input', (event) => {
        header[event.target.dataset.field] = event.target.value;
        updatePreview();
      });
    });

    row.querySelector('.remove-row').addEventListener('click', () => {
      endpoint.headers.splice(index, 1);
      renderEndpoints();
      updatePreview();
    });

    container.appendChild(row);
  });

  if (endpoint.headers.length === 0) {
    const hint = document.createElement('p');
    hint.className = 'empty-hint';
    hint.textContent = '还没有请求头，可以点击“添加请求头”。';
    container.appendChild(hint);
  }
}

function renderParameterRows(node, endpoint) {
  const container = node.querySelector('[data-collection="parameters"]');
  container.innerHTML = '';
  endpoint.parameters.forEach((parameter, index) => {
    const row = parameterRowTemplate.content.cloneNode(true).firstElementChild;
    row.querySelector('[data-field="name"]').value = parameter.name;
    row.querySelector('[data-field="type"]').value = parameter.type;
    row.querySelector('[data-field="required"]').value = parameter.required;
    row.querySelector('[data-field="description"]').value = parameter.description;

    row.querySelectorAll('[data-field]').forEach((input) => {
      const field = input.dataset.field;
      const eventName = input.tagName === 'SELECT' ? 'change' : 'input';
      input.addEventListener(eventName, (event) => {
        parameter[field] = event.target.value;
        updatePreview();
      });
    });

    row.querySelector('.remove-row').addEventListener('click', () => {
      endpoint.parameters.splice(index, 1);
      renderEndpoints();
      updatePreview();
    });

    container.appendChild(row);
  });

  if (endpoint.parameters.length === 0) {
    const hint = document.createElement('p');
    hint.className = 'empty-hint';
    hint.textContent = '请求体字段将在这里展示，可以点击“添加字段”。';
    container.appendChild(hint);
  }
}

function updatePreview() {
  markdownPreview.textContent = generateMarkdown(state);
}

function generateMarkdown(data) {
  const lines = [];
  const title = data.title.trim() || '未命名接口文档';
  lines.push(`# ${title}`);
  if (data.description.trim()) {
    lines.push('', data.description.trim());
  }

  data.endpoints.forEach((endpoint, index) => {
    lines.push('', `## ${index + 1}. ${endpoint.name.trim() || '未命名接口'}`);
    if (endpoint.summary.trim()) {
      lines.push('', endpoint.summary.trim());
    }

    if (endpoint.method.trim()) {
      lines.push('', `- **请求方式**: \`${endpoint.method.trim()}\``);
    }
    if (endpoint.path.trim()) {
      lines.push(`- **请求路径**: \`${endpoint.path.trim()}\``);
    }

    const validHeaders = endpoint.headers.filter(
      (header) => header.name.trim() || header.value.trim() || header.description.trim()
    );
    if (validHeaders.length) {
      lines.push('- **请求头**:');
      validHeaders.forEach((header) => {
        const name = header.name.trim();
        const value = header.value.trim();
        const desc = header.description.trim();
        let line = `  - \`${name || 'Header'}\``;
        if (value) {
          line += `: ${value}`;
        }
        if (desc) {
          line += ` - ${desc}`;
        }
        lines.push(line);
      });
    }

    const validParameters = endpoint.parameters.filter(
      (param) => param.name.trim() || param.type.trim() || param.description.trim()
    );

    if (validParameters.length) {
      lines.push('', '#### 请求体参数', '');
      lines.push('| 字段名 | 类型 | 必填 | 说明 |');
      lines.push('| ------ | ---- | ---- | ---- |');
      validParameters.forEach((param) => {
        const required = param.required === 'yes' ? '是' : '否';
        lines.push(
          `| \`${param.name.trim() || '-'}\` | \`${param.type.trim() || '-'}\` | ${required} | ${
            param.description.trim() || '-'
          } |`
        );
      });
    }

    if (endpoint.requestExample.trim()) {
      lines.push('', '#### 请求示例', '');
      lines.push(...renderCodeBlock(endpoint.requestExample));
    }

    if (endpoint.responseExample.trim()) {
      lines.push('', '#### 响应示例', '');
      lines.push(...renderCodeBlock(endpoint.responseExample));
    }
  });

  return lines.join('\n');
}

function renderCodeBlock(content) {
  const lines = [];
  const language = detectLanguage(content);
  lines.push(`\`\`\`${language}`.trimEnd());
  lines.push(content.trim());
  lines.push('```');
  return lines;
}

function detectLanguage(content) {
  const trimmed = content.trim();
  if (!trimmed) return '';
  if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
    return 'JSON';
  }
  if (/^curl\s/i.test(trimmed)) {
    return 'bash';
  }
  if (trimmed.startsWith('<')) {
    return 'xml';
  }
  return '';
}

function loadFromOpenApi(document) {
  if (!document || typeof document !== 'object') {
    throw new Error('Invalid OpenAPI document');
  }

  const info = document.info || {};
  state.title = info.title || '未命名接口文档';
  state.description = info.description || '';

  const endpoints = [];
  endpointCounter = 1;

  if (document.paths && typeof document.paths === 'object') {
    Object.entries(document.paths).forEach(([path, operations]) => {
      if (!operations || typeof operations !== 'object') return;
      Object.entries(operations).forEach(([method, details]) => {
        if (!isHttpMethod(method) || !details || typeof details !== 'object') return;
        const endpoint = createEndpoint();
        endpoint.name = details.summary || details.operationId || `${method.toUpperCase()} ${path}`;
        endpoint.method = method.toUpperCase();
        endpoint.path = path;
        endpoint.summary = details.description || details.summary || '';

        const aggregatedParameters = collectParameters(operations.parameters, details.parameters);
        endpoint.headers = aggregatedParameters.headers;
        endpoint.parameters = aggregatedParameters.parameters;

        const requestBody = details.requestBody;
        if (requestBody) {
          const example = extractBodyExample(requestBody);
          if (example) {
            endpoint.requestExample = example;
          }
          const schemaParameters = parseSchemaParameters(requestBody);
          if (schemaParameters.length) {
            endpoint.parameters = mergeParameters(endpoint.parameters, schemaParameters);
          }
        }

        const responseExample = extractResponseExample(details.responses);
        if (responseExample) {
          endpoint.responseExample = responseExample;
        }

        endpoints.push(endpoint);
      });
    });
  }

  state.endpoints = endpoints.length ? endpoints : [createEndpoint()];
  titleInput.value = state.title;
  descriptionInput.value = state.description;
  renderEndpoints();
  updatePreview();
}

function isHttpMethod(value) {
  return ['get', 'post', 'put', 'patch', 'delete', 'options', 'head'].includes(String(value).toLowerCase());
}

function collectParameters(pathParameters = [], operationParameters = []) {
  const headers = [];
  const parameters = [];
  const merged = [...(Array.isArray(pathParameters) ? pathParameters : []), ...(Array.isArray(operationParameters) ? operationParameters : [])];

  merged.forEach((param) => {
    if (!param || typeof param !== 'object') return;
    const target = String(param.in).toLowerCase();
    const entry = {
      name: param.name || '',
      type: inferSchemaType(param.schema),
      required: param.required ? 'yes' : 'no',
      description: param.description || '',
    };

    if (target === 'header') {
      headers.push({
        name: param.name || '',
        value: param.example ?? (param.schema ? param.schema.example ?? param.schema.default : ''),
        description: param.description || '',
      });
    } else {
      parameters.push(entry);
    }
  });

  return { headers, parameters };
}

function parseSchemaParameters(requestBody) {
  const content = requestBody.content || {};
  const mediaTypes = ['application/json', 'application/x-www-form-urlencoded', 'multipart/form-data'];
  const schema = mediaTypes
    .map((type) => content[type]?.schema)
    .find((item) => item && typeof item === 'object');

  if (!schema) return [];

  const requiredSet = new Set(Array.isArray(schema.required) ? schema.required : []);
  if (schema.type === 'object' && schema.properties && typeof schema.properties === 'object') {
    return Object.entries(schema.properties).map(([name, propertySchema]) => ({
      name,
      type: propertySchema.type || inferSchemaType(propertySchema),
      required: requiredSet.has(name) ? 'yes' : 'no',
      description: propertySchema.description || '',
    }));
  }

  return [];
}

function inferSchemaType(schema) {
  if (!schema || typeof schema !== 'object') return '-';
  if (schema.type) return schema.type;
  if (schema.properties) return 'object';
  if (schema.items) return 'array';
  return '-';
}

function extractBodyExample(requestBody) {
  const content = requestBody.content || {};
  const example = getExampleFromContent(content);
  return example ? JSON.stringify(example, null, 2) : '';
}

function extractResponseExample(responses) {
  if (!responses || typeof responses !== 'object') return '';
  const firstResponse = Object.values(responses).find((resp) => resp && typeof resp === 'object');
  if (!firstResponse) return '';
  const content = firstResponse.content || {};
  const example = getExampleFromContent(content);
  return example ? JSON.stringify(example, null, 2) : '';
}

function getExampleFromContent(content) {
  const preferredTypes = ['application/json', 'application/*+json'];
  let payload;
  for (const type of preferredTypes) {
    if (content[type]) {
      payload = content[type];
      break;
    }
  }
  if (!payload) {
    payload = Object.values(content)[0];
  }
  if (!payload) return null;

  if (payload.example) return payload.example;
  if (payload.examples) {
    const firstExample = Object.values(payload.examples)[0];
    if (firstExample && typeof firstExample === 'object') {
      return firstExample.value || null;
    }
  }
  if (payload.schema && payload.schema.example) return payload.schema.example;
  return null;
}

function mergeParameters(existing, additional) {
  const seen = new Set();
  const result = [];

  [...existing, ...additional].forEach((param) => {
    const key = `${param.name || ''}-${param.type || ''}`;
    if (seen.has(key)) return;
    seen.add(key);
    result.push(param);
  });

  return result;
}

document.getElementById('add-endpoint').addEventListener('click', () => {
  state.endpoints.push(createEndpoint());
  renderEndpoints();
  updatePreview();
});

document.getElementById('copy-markdown').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(markdownPreview.textContent);
    showToast('Markdown 已复制到剪贴板');
  } catch (error) {
    showToast('复制失败，请手动复制', true);
  }
});

titleInput.addEventListener('input', (event) => {
  state.title = event.target.value;
  updatePreview();
});

descriptionInput.addEventListener('input', (event) => {
  state.description = event.target.value;
  updatePreview();
});

function showToast(message, isError = false) {
  const toast = document.createElement('div');
  toast.className = `toast ${isError ? 'error' : ''}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.add('visible');
  });
  setTimeout(() => {
    toast.classList.remove('visible');
    setTimeout(() => toast.remove(), 300);
  }, 2200);
}

function bootstrap() {
  if (state.endpoints.length === 0) {
    const endpoint = createEndpoint();
    endpoint.headers.push({ name: 'Content-type', value: 'application/json', description: '' });
    endpoint.headers.push({ name: 'Authorization', value: 'Bearer {token}', description: '' });
    state.endpoints.push(endpoint);
  }
  renderEndpoints();
  updatePreview();
}

if (importButton && importInput) {
  importButton.addEventListener('click', () => {
    importInput.click();
  });

  importInput.addEventListener('change', async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const text = await file.text();
      const json = JSON.parse(text);
      loadFromOpenApi(json);
      showToast(`已导入 ${file.name}`);
    } catch (error) {
      console.error(error);
      showToast('导入失败，请确认文件是有效的 OpenAPI JSON', true);
    } finally {
      importInput.value = '';
    }
  });
}

bootstrap();
