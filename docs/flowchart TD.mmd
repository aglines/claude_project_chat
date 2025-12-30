flowchart TD
    %% User Entry Points
    Start([User Opens Browser]) --> LoadUI[Load index.html]
    LoadUI --> InitApp[Initialize app.js]
    
    %% UI Initialization
    InitApp --> CheckMode{Check Connection Mode}
    CheckMode -->|Web Client| WebMode[Display Projects Mode]
    CheckMode -->|API Client| APIMode[Display API Mode]
    
    %% Main UI Components
    WebMode --> UIReady[UI Ready]
    APIMode --> UIReady
    UIReady --> TabChoice{User Selects Tab}
    
    %% Template Mode Flow
    TabChoice -->|Templates Tab| TemplateUI[prompt-builder.js]
    TemplateUI --> SelectTemplate[Select Template Category]
    SelectTemplate --> FillVars[Fill Template Variables]
    FillVars --> TemplateFiles{Upload Files?}
    TemplateFiles -->|Yes| UploadTemplate[File Upload Handler]
    TemplateFiles -->|No| CompilePrompt
    UploadTemplate --> CompilePrompt[Compile Prompt]
    CompilePrompt --> SendTemplate[Send to /api/chat]
    
    %% Simple Mode Flow
    TabChoice -->|Simple Input Tab| SimpleUI[Simple Input Form]
    SimpleUI --> SelectPrompt[Select Prompt Dropdown]
    SelectPrompt --> EnterMsg[Enter Message]
    EnterMsg --> SimpleFiles{Upload Files?}
    SimpleFiles -->|Yes| UploadSimple[File Upload Handler]
    SimpleFiles -->|No| SendSimple[Send to /api/chat]
    UploadSimple --> SendSimple
    
    %% Backend Processing
    SendTemplate --> APIChat[app.py: /api/chat]
    SendSimple --> APIChat
    
    APIChat --> GetClient{Get Claude Client}
    GetClient -->|Web Mode| WebClient[claude_web_client.py]
    GetClient -->|API Mode| APIClient[claude_client.py]
    
    %% File Processing
    APIChat --> CheckFiles{Files Attached?}
    CheckFiles -->|Yes| ProcessFiles[file_processor.py]
    ProcessFiles --> ExtractContent[Extract Text/Content]
    ExtractContent --> BuildMessage
    CheckFiles -->|No| BuildMessage[Build Message Payload]
    
    %% Claude Communication
    BuildMessage --> WebClient
    BuildMessage --> APIClient
    
    WebClient --> WebAPI[Claude.ai Web API]
    APIClient --> OfficialAPI[Anthropic Official API]
    
    %% Tool Execution
    WebAPI --> ToolCheck{Tools Needed?}
    OfficialAPI --> ToolCheck
    
    ToolCheck -->|Web Fetch| FetchURL[url_fetcher.py]
    ToolCheck -->|Web Search| SearchWeb[tool_handler.py]
    ToolCheck -->|No Tools| GetResponse
    
    FetchURL --> GetResponse[Get Claude Response]
    SearchWeb --> GetResponse
    
    %% Response Handling
    GetResponse --> ReturnJSON[Return JSON Response]
    ReturnJSON --> UpdateUI[app.js: Update Chat UI]
    UpdateUI --> DisplayMsg[Display Message in Chat]
    DisplayMsg --> ShowStats{Tool Stats?}
    
    ShowStats -->|Yes| DisplayStats[Show Fetch/Search Stats]
    ShowStats -->|No| Ready
    DisplayStats --> Ready[Ready for Next Input]
    
    %% Additional Features
    Ready --> UserAction{User Action}
    UserAction -->|New Message| TabChoice
    UserAction -->|New Chat| NewConv[Create New Conversation]
    UserAction -->|Clear Chat| ClearSession[Clear Session History]
    UserAction -->|Switch Project| ProjectMgr[Project Manager]
    UserAction -->|Settings| SettingsModal[Template Settings]
    
    %% Project Management
    ProjectMgr --> ListProjects[ /api/projects]
    ListProjects --> SetActive[ /api/projects/set-active]
    SetActive --> UpdateClient[Update Web Client Context]
    UpdateClient --> Ready
    
    %% Settings & Configuration
    SettingsModal --> ManageTemplates[Custom Templates]
    SettingsModal --> SwitchMode[Switch API/Web Mode]
    SwitchMode --> CheckMode
    
    %% Configuration Layer
    Config[project_config.yaml] -.->|UI Settings| LoadUI
    Config -.->|Prompts| SimpleUI
    Config -.->|Features| UIReady
    Env[.env] -.->|API Keys/Cookies| GetClient
    Templates[custom_prompts.yaml] -.->|Custom Templates| TemplateUI
    
    %% Styling
    classDef userAction fill:#3b82f6,stroke:#1e40af,color:#fff
    classDef backend fill:#10b981,stroke:#059669,color:#fff
    classDef external fill:#f59e0b,stroke:#d97706,color:#fff
    classDef config fill:#8b5cf6,stroke:#6d28d9,color:#fff
    classDef storage fill:#ec4899,stroke:#db2777,color:#fff
    
    class Start,TabChoice,UserAction userAction
    class APIChat,GetClient,ProcessFiles,BuildMessage backend
    class WebAPI,OfficialAPI,FetchURL,SearchWeb external
    class Config,Env,Templates config
    class NewConv,ClearSession,ProjectMgr storage