# MCP Server Example Payloads

This document provides example payloads for different operations in the Model Context Protocol (MCP) server.

## 1. Context Creation

### Request
```http
POST /api/v1/context
Content-Type: application/json
Authorization: Basic <base64-encoded-credentials>

{
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "sessionId": "session-123",
    "initialContext": {
        "systemPrompt": "You are a helpful AI assistant.",
        "conversationHistory": [
            {
                "role": "user",
                "content": "Hello, how can you help me?"
            },
            {
                "role": "assistant",
                "content": "I can help you with various tasks. What would you like to do?"
            }
        ],
        "metadata": {
            "source": "web-interface",
            "userPreferences": {
                "language": "en",
                "tone": "professional"
            }
        }
    },
    "ttl": 3600
}
```

### Response
```json
{
    "contextId": "ctx-abc123",
    "status": "created",
    "createdAt": "2024-03-20T10:00:00Z",
    "expiresAt": "2024-03-20T11:00:00Z",
    "size": 1024
}
```

## 2. Context Retrieval

### Request
```http
GET /api/v1/context/ctx-abc123
Authorization: Basic <base64-encoded-credentials>
```

### Response
```json
{
    "contextId": "ctx-abc123",
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "sessionId": "session-123",
    "currentContext": {
        "systemPrompt": "You are a helpful AI assistant.",
        "conversationHistory": [
            {
                "role": "user",
                "content": "Hello, how can you help me?"
            },
            {
                "role": "assistant",
                "content": "I can help you with various tasks. What would you like to do?"
            }
        ],
        "metadata": {
            "source": "web-interface",
            "userPreferences": {
                "language": "en",
                "tone": "professional"
            }
        }
    },
    "createdAt": "2024-03-20T10:00:00Z",
    "expiresAt": "2024-03-20T11:00:00Z",
    "size": 1024
}
```

## 3. Context Update

### Request
```http
PUT /api/v1/context/ctx-abc123
Content-Type: application/json
Authorization: Basic <base64-encoded-credentials>

{
    "update": {
        "conversationHistory": [
            {
                "role": "user",
                "content": "Can you help me with Python programming?"
            }
        ]
    },
    "metadata": {
        "lastInteraction": "2024-03-20T10:05:00Z"
    }
}
```

### Response
```json
{
    "contextId": "ctx-abc123",
    "status": "updated",
    "updatedAt": "2024-03-20T10:05:00Z",
    "size": 1536
}
```

## 4. Model Interaction with Context

### Request
```http
POST /api/v1/model/interact
Content-Type: application/json
Authorization: Basic <base64-encoded-credentials>

{
    "contextId": "ctx-abc123",
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "input": {
        "role": "user",
        "content": "Can you help me with Python programming?"
    },
    "parameters": {
        "temperature": 0.7,
        "maxTokens": 1000
    }
}
```

### Response
```json
{
    "interactionId": "int-xyz789",
    "contextId": "ctx-abc123",
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "response": {
        "role": "assistant",
        "content": "I'd be happy to help you with Python programming! What specific aspect would you like to learn about? I can help with:\n\n1. Basic syntax and data types\n2. Control structures\n3. Functions and modules\n4. Object-oriented programming\n5. File handling\n6. Error handling\n\nLet me know what interests you most!"
    },
    "metadata": {
        "tokensUsed": 150,
        "processingTime": 0.8,
        "timestamp": "2024-03-20T10:05:05Z"
    }
}
```

## 5. Context Search

### Request
```http
POST /api/v1/context/search
Content-Type: application/json
Authorization: Basic <base64-encoded-credentials>

{
    "query": "Python programming",
    "filters": {
        "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
        "dateRange": {
            "from": "2024-03-19T00:00:00Z",
            "to": "2024-03-20T23:59:59Z"
        }
    },
    "limit": 10
}
```

### Response
```json
{
    "results": [
        {
            "contextId": "ctx-abc123",
            "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
            "sessionId": "session-123",
            "summary": {
                "firstMessage": "Hello, how can you help me?",
                "lastMessage": "Can you help me with Python programming?",
                "messageCount": 3
            },
            "createdAt": "2024-03-20T10:00:00Z",
            "lastUpdated": "2024-03-20T10:05:00Z"
        }
    ],
    "total": 1,
    "page": 1,
    "pageSize": 10
}
```

## 6. Context Deletion

### Request
```http
DELETE /api/v1/context/ctx-abc123
Authorization: Basic <base64-encoded-credentials>
```

### Response
```json
{
    "contextId": "ctx-abc123",
    "status": "deleted",
    "deletedAt": "2024-03-20T10:10:00Z"
}
```

## 7. Batch Context Operations

### Request
```http
POST /api/v1/context/batch
Content-Type: application/json
Authorization: Basic <base64-encoded-credentials>

{
    "operations": [
        {
            "type": "create",
            "data": {
                "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
                "sessionId": "session-456",
                "initialContext": {
                    "systemPrompt": "You are a technical assistant."
                }
            }
        },
        {
            "type": "update",
            "contextId": "ctx-abc123",
            "data": {
                "metadata": {
                    "tags": ["python", "programming"]
                }
            }
        }
    ]
}
```

### Response
```json
{
    "results": [
        {
            "operation": "create",
            "status": "success",
            "contextId": "ctx-def456",
            "createdAt": "2024-03-20T10:15:00Z"
        },
        {
            "operation": "update",
            "status": "success",
            "contextId": "ctx-abc123",
            "updatedAt": "2024-03-20T10:15:00Z"
        }
    ],
    "batchId": "batch-123",
    "completedAt": "2024-03-20T10:15:01Z"
}
```

## Error Responses

### Rate Limit Exceeded
```json
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "Too many requests. Please try again in 60 seconds.",
        "retryAfter": 60
    }
}
```

### Context Not Found
```json
{
    "error": {
        "code": "CONTEXT_NOT_FOUND",
        "message": "Context with ID ctx-xyz789 not found",
        "contextId": "ctx-xyz789"
    }
}
```

### Invalid Context Size
```json
{
    "error": {
        "code": "CONTEXT_SIZE_EXCEEDED",
        "message": "Context size exceeds maximum allowed size of 1024KB",
        "currentSize": 2048,
        "maxSize": 1024
    }
}
``` 