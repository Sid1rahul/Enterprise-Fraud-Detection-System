import React, { useState, useEffect, useRef } from 'react';
import { 
  MessageCircle, 
  X, 
  Send, 
  Bot, 
  User,
  Minimize2,
  Maximize2,
  AlertTriangle,
  CheckCircle,
  Activity,
  FileText,
  Mic,
  Square,
  Volume2
} from 'lucide-react';
import { fraudAPI } from '../utils/api';
import './FraudChatbot.css';

const FraudChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [isVoiceSupported, setIsVoiceSupported] = useState(false);
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recognitionRef = useRef(null);
  const recordingIntervalRef = useRef(null);

  // UiPath Studio connection status
  const [uiPathStatus, setUiPathStatus] = useState('disconnected');
  const [uiPathWorkflow, setUiPathWorkflow] = useState(null);

  useEffect(() => {
    // Initialize chatbot with welcome message
    if (messages.length === 0) {
      setMessages([
        {
          id: 1,
          type: 'bot',
          message: '🤖 Hi! I\'m your Fraud Detection Assistant. I can help you analyze transactions, check system status, or guide you through the platform. You can type or use voice!',
          timestamp: new Date().toISOString(),
          suggestions: [
            'Check system health',
            'Analyze a transaction',
            'Show fraud statistics',
            'Upload transaction file'
          ]
        }
      ]);
    }

    // Check voice support
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    setIsVoiceSupported(!!SpeechRecognition);
    
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-US';
      
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInputMessage(transcript);
        stopRecording();
      };
      
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        stopRecording();
      };
    }

    // Check UiPath Studio connection
    checkUiPathConnection();
    
    return () => {
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
    };
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const checkUiPathConnection = async () => {
    try {
      // Check if UiPath Studio is connected via local API endpoint
      const response = await fetch('http://localhost:8001/uipath/status', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      
      if (response.ok) {
        const data = await response.json();
        setUiPathStatus('connected');
        setUiPathWorkflow(data.workflow);
        setIsConnected(true);
      }
    } catch (error) {
      setUiPathStatus('disconnected');
      setIsConnected(false);
    }
  };

  const parseIntent = (message) => {
    const lowerMessage = message.toLowerCase();
    
    // Greeting intents
    if (lowerMessage.match(/^(hi|hello|hey|good morning|good afternoon|good evening)$/i)) {
      return { type: 'greeting' };
    }
    
    // Gratitude intents
    if (lowerMessage.match(/thank you|thanks|thx|appreciate|grateful|cheers/i)) {
      return { type: 'gratitude' };
    }
    
    // Farewell intents
    if (lowerMessage.match(/bye|goodbye|see you|farewell|take care|later|exit|quit/i)) {
      return { type: 'farewell' };
    }
    
    // Help intents
    if (lowerMessage.match(/help|what can you do|capabilities|commands|assist/i)) {
      return { type: 'help' };
    }
    
    // Transaction analysis intent
    if (lowerMessage.match(/analyze|check.*\$?\d+|fraud.*\$?\d+/i)) {
      const amountMatch = message.match(/\$?(\d+(?:\.\d{2})?)/);
      const merchantMatch = message.match(/at\s+([^,\s]+(?:\s+[^,\s]+)*)/i);
      
      return {
        type: 'transaction_analysis',
        data: {
          amount: amountMatch ? parseFloat(amountMatch[1]) : 1000,
          merchant: merchantMatch ? merchantMatch[1] : 'Unknown Merchant'
        }
      };
    }
    
    // System status intent
    if (lowerMessage.match(/status|health|system|working|online/i)) {
      return { type: 'system_status' };
    }
    
    // Navigation intent
    if (lowerMessage.match(/go to|navigate|show|open|upload|file/i)) {
      return { type: 'navigation', data: lowerMessage };
    }
    
    // Statistics intent
    if (lowerMessage.match(/statistics|stats|fraud rate|metrics/i)) {
      return { type: 'statistics' };
    }
    
    // Compliment intents
    if (lowerMessage.match(/good job|well done|excellent|amazing|awesome|great|nice|perfect/i)) {
      return { type: 'compliment' };
    }
    
    return { type: 'unknown' };
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      message: inputMessage,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Process message and get bot response
    const botResponse = await processMessage(inputMessage);
    
    setTimeout(() => {
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1000);

    // Send to UiPath Studio if connected
    if (isConnected) {
      sendToUiPath(userMessage, botResponse);
    }
  };

  const processMessage = async (message) => {
    const intent = parseIntent(message);
    let responseMessage = '';
    let suggestions = [];

    try {
      switch (intent.type) {
        case 'greeting':
          responseMessage = getGreetingMessage();
          suggestions = ['Check system health', 'Analyze a transaction', 'Show me around'];
          break;
          
        case 'gratitude':
          responseMessage = getGratitudeResponse();
          suggestions = ['Analyze another transaction', 'Check system status', 'Need more help?'];
          break;
          
        case 'farewell':
          responseMessage = getFarewellMessage();
          suggestions = ['Actually, one more thing...', 'Check system before leaving', 'See you later!'];
          break;
          
        case 'help':
          responseMessage = getHelpMessage();
          suggestions = ['Check system health', 'Analyze transaction', 'Show statistics'];
          break;
          
        case 'compliment':
          responseMessage = getComplimentResponse();
          suggestions = ['Analyze a transaction', 'Show system status', 'What else can you do?'];
          break;
          
        case 'transaction_analysis':
          responseMessage = await analyzeTransaction(intent.data);
          suggestions = ['Check another transaction', 'Show system status', 'Go to batch processing'];
          break;
          
        case 'system_status':
          responseMessage = await getSystemStatus();
          suggestions = ['Analyze a transaction', 'Show fraud statistics', 'Upload file'];
          break;
          
        case 'navigation':
          responseMessage = handleNavigation(intent.data);
          suggestions = ['Analyze transaction', 'Check system health', 'Show statistics'];
          break;
          
        case 'statistics':
          responseMessage = await getFraudStatistics();
          suggestions = ['Analyze transaction', 'Check system status', 'Upload file'];
          break;
          
        default:
          responseMessage = getUnknownResponse();
          suggestions = ['Check system health', 'Analyze transaction', 'Show statistics'];
      }
    } catch (error) {
      responseMessage = '❌ Sorry, I encountered an error. Please make sure the fraud detection system is running.';
      suggestions = ['Try again', 'Check system status'];
    }

    return {
      id: Date.now() + 1,
      type: 'bot',
      message: responseMessage,
      timestamp: new Date().toISOString(),
      suggestions
    };
  };

  const analyzeTransaction = async (data) => {
    try {
      const response = await fraudAPI.predictFraud({
        amount: data.amount,
        merchant: data.merchant,
        cardType: 'credit',
        customerId: `CUST_${Math.floor(Math.random() * 10000)}`
      });

      const riskLevel = response.fraud_probability > 0.7 ? 'HIGH' : 
                       response.fraud_probability > 0.3 ? 'MEDIUM' : 'LOW';
      
      const prediction = response.is_fraud ? 'FRAUD' : response.decision || 'ALLOW';
      const icon = response.is_fraud ? '🚨' : 
                   response.fraud_probability > 0.3 ? '⚠️' : '✅';

      return `${icon} **Transaction Analysis Complete**

💰 **Amount**: $${data.amount.toFixed(2)}
🏪 **Merchant**: ${data.merchant}
📊 **Fraud Probability**: ${(response.fraud_probability * 100).toFixed(1)}%
⚡ **Risk Level**: ${riskLevel}
🎯 **Recommendation**: ${prediction}

**Case ID**: TXN_${Date.now()}`;
    } catch (error) {
      return `❌ Unable to analyze transaction. Error: ${error.message}`;
    }
  };

  const getSystemStatus = async () => {
    try {
      const health = await fraudAPI.healthCheck();
      const modelStatus = await fraudAPI.getModelStatus();
      
      return `✅ **System Status: HEALTHY**

🔧 **API Status**: ${health.status}
🤖 **Models Loaded**: ${modelStatus.models_loaded.join(', ')}
⏰ **Last Updated**: ${new Date(health.timestamp).toLocaleTimeString()}
🌐 **Endpoint**: http://localhost:5000
${isConnected ? '🔗 **UiPath**: Connected' : '⚠️ **UiPath**: Disconnected'}

All systems are operational and ready for fraud detection!`;
    } catch (error) {
      return `❌ **System Status: ERROR**

The fraud detection system appears to be offline. Please check:
- Backend API is running on port 5000
- All required services are started
- Network connectivity is available`;
    }
  };

  const getFraudStatistics = async () => {
    try {
      // Mock statistics for demo - in real implementation, get from API
      const stats = {
        totalTransactions: Math.floor(Math.random() * 10000) + 5000,
        fraudDetected: Math.floor(Math.random() * 500) + 100,
        avgProcessingTime: Math.floor(Math.random() * 50) + 25
      };
      
      const fraudRate = ((stats.fraudDetected / stats.totalTransactions) * 100).toFixed(2);
      
      return `📊 **Fraud Detection Statistics**

📈 **Total Transactions**: ${stats.totalTransactions.toLocaleString()}
🚨 **Fraud Detected**: ${stats.fraudDetected.toLocaleString()}
📉 **Fraud Rate**: ${fraudRate}%
⚡ **Avg Processing Time**: ${stats.avgProcessingTime}ms
🎯 **Accuracy**: 95.2%

**Today's Performance**: Excellent - All systems operating within normal parameters.`;
    } catch (error) {
      return `❌ Unable to retrieve statistics. Please check system status.`;
    }
  };

  const handleNavigation = (message) => {
    if (message.includes('upload') || message.includes('file')) {
      return `📁 **File Upload Guide**

To upload transaction files:
1. Go to **Real-Time Monitoring** page
2. Click the upload area or drag & drop your file
3. Supported formats: CSV, Excel (.xlsx, .xls)
4. Required columns: Amount, Merchant, Customer_ID, Timestamp, Card_Type

Would you like me to guide you there?`;
    }
    
    if (message.includes('batch') || message.includes('multiple')) {
      return `📦 **Batch Processing Guide**

To process multiple transactions:
1. Navigate to **Batch Processing** page
2. Add transactions manually or use the template
3. Click "Process Batch" to analyze all transactions
4. View results and export if needed

The batch processor can handle up to 100 transactions at once.`;
    }
    
    return `🧭 **Navigation Help**

Available pages:
- **Dashboard**: System overview and metrics
- **Fraud Detection**: Single transaction analysis
- **Batch Processing**: Multiple transaction handling
- **Real-Time Monitoring**: File upload and live processing
- **Analytics**: Advanced reporting
- **Settings**: System configuration

What would you like to explore?`;
  };

  const getGreetingMessage = () => {
    const greetings = [
      `👋 Hello! I'm your AI-powered fraud detection assistant. How can I help you today?`,
      `🤖 Hi there! Ready to tackle some fraud detection? What would you like to explore?`,
      `✨ Welcome! I'm here to help you navigate the fraud detection system. What's on your mind?`,
      `🛡️ Greetings! Your fraud detection assistant is ready. How may I assist you?`
    ];
    return greetings[Math.floor(Math.random() * greetings.length)];
  };

  const getGratitudeResponse = () => {
    const responses = [
      `😊 You're very welcome! I'm always happy to help with fraud detection. Is there anything else you'd like to explore?`,
      `🙏 My pleasure! That's what I'm here for. Feel free to ask if you need help with anything else.`,
      `✨ Glad I could help! Don't hesitate to reach out if you have more questions about the system.`,
      `🤖 Anytime! I love helping users navigate fraud detection. What else can I assist you with?`,
      `💙 You're so kind! I'm here whenever you need fraud detection support.`
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const getFarewellMessage = () => {
    const farewells = [
      `👋 Goodbye! Thanks for using the fraud detection system. Stay vigilant against fraud!`,
      `🛡️ Take care! Remember, I'm always here when you need fraud detection assistance.`,
      `✨ See you later! Keep those transactions secure and don't hesitate to come back anytime.`,
      `🤖 Farewell! It was great helping you today. Until next time, stay fraud-free!`,
      `💙 Bye for now! Thanks for making the digital world a safer place. Come back soon!`
    ];
    return farewells[Math.floor(Math.random() * farewells.length)];
  };

  const getComplimentResponse = () => {
    const responses = [
      `😊 Thank you so much! I do my best to help keep your transactions safe. Your feedback means a lot!`,
      `🤖 Aww, you're too kind! I'm just doing what I love - protecting against fraud. Glad you're happy!`,
      `✨ That really brightens my day! I'm passionate about fraud detection and love helping users like you.`,
      `💙 You're amazing too! Together we make a great fraud-fighting team. What else can we tackle?`,
      `🛡️ Thanks! I'm constantly learning to better serve fraud detection needs. Your encouragement helps!`
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const getUnknownResponse = () => {
    const responses = [
      `🤔 I'm not quite sure I understand that. Could you try rephrasing? I'm great with fraud detection questions!`,
      `🤖 Hmm, that's a bit outside my expertise. I specialize in fraud detection - try asking about transactions or system status!`,
      `💭 I didn't catch that. I'm best at helping with fraud analysis, system health, and navigation. What would you like to know?`,
      `🔍 That's interesting, but I'm focused on fraud detection. Ask me about analyzing transactions or checking system status!`
    ];
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const getHelpMessage = () => {
    return `🤖 **How I Can Help You**

I can assist with:
- 🔍 **Transaction Analysis**: "Check $500 at Amazon for fraud"
- 📊 **System Status**: "Is the system healthy?"
- 📈 **Statistics**: "Show fraud detection stats"
- 🧭 **Navigation**: "How do I upload a file?"
- 📁 **File Processing**: "Guide me through batch processing"

**I also understand:**
- Greetings: "Hi", "Hello", "Good morning"
- Thanks: "Thank you", "Thanks", "Appreciate it"
- Goodbyes: "Bye", "See you later", "Take care"

Just type naturally, and I'll help you out! 😊`;
  };

  const sendToUiPath = async (userMessage, botResponse) => {
    try {
      await fetch('http://localhost:8001/uipath/conversation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_message: userMessage.message,
          bot_response: botResponse.message,
          timestamp: new Date().toISOString(),
          session_id: 'fraud_detection_chat'
        })
      });
    } catch (error) {
      console.log('UiPath not connected:', error);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setInputMessage(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const startRecording = () => {
    if (!isVoiceSupported || !recognitionRef.current) {
      alert('Voice recognition is not supported in your browser. Please use Chrome or Edge.');
      return;
    }

    try {
      setIsRecording(true);
      setRecordingTime(0);
      
      // Start recording timer
      recordingIntervalRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      
      // Start speech recognition
      recognitionRef.current.start();
    } catch (error) {
      console.error('Error starting recording:', error);
      stopRecording();
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    setRecordingTime(0);
    
    if (recordingIntervalRef.current) {
      clearInterval(recordingIntervalRef.current);
      recordingIntervalRef.current = null;
    }
    
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (error) {
        console.error('Error stopping recognition:', error);
      }
    }
  };

  const handleVoiceButtonClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const formatRecordingTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!isOpen) {
    return (
      <div className="chatbot-trigger" onClick={() => setIsOpen(true)}>
        <MessageCircle size={24} />
        <div className="trigger-pulse"></div>
        {isConnected && <div className="uipath-indicator">UiPath</div>}
      </div>
    );
  }

  return (
    <div className={`chatbot-container ${isMinimized ? 'minimized' : ''}`}>
      <div className="chatbot-header">
        <div className="header-info">
          <Bot size={20} />
          <div>
            <h4>Fraud Assistant</h4>
            <span className={`status ${isConnected ? 'connected' : 'offline'}`}>
              {isConnected ? '🔗 UiPath Connected' : '⚠️ Standalone Mode'}
            </span>
          </div>
        </div>
        <div className="header-controls">
          <button 
            onClick={() => setIsMinimized(!isMinimized)}
            className="control-btn"
          >
            {isMinimized ? <Maximize2 size={16} /> : <Minimize2 size={16} />}
          </button>
          <button 
            onClick={() => setIsOpen(false)}
            className="control-btn close"
          >
            <X size={16} />
          </button>
        </div>
      </div>

      {!isMinimized && (
        <>
          <div className="chatbot-messages">
            {messages.map((msg) => (
              <div key={msg.id} className={`message ${msg.type}`}>
                <div className="message-avatar">
                  {msg.type === 'bot' ? <Bot size={16} /> : <User size={16} />}
                </div>
                <div className="message-content">
                  <div className="message-text">
                    {msg.message.split('\n').map((line, index) => (
                      <div key={index}>{line}</div>
                    ))}
                  </div>
                  {msg.suggestions && (
                    <div className="message-suggestions">
                      {msg.suggestions.map((suggestion, index) => (
                        <button
                          key={index}
                          className="suggestion-btn"
                          onClick={() => handleSuggestionClick(suggestion)}
                        >
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                  <div className="message-time">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="message bot typing">
                <div className="message-avatar">
                  <Bot size={16} />
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input">
            {isRecording && (
              <div className="recording-indicator">
                <Volume2 size={16} className="recording-icon" />
                <span>{formatRecordingTime(recordingTime)}</span>
              </div>
            )}
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isRecording ? "Listening..." : "Type or speak your message..."}
              className="message-input"
              disabled={isRecording}
            />
            {isVoiceSupported && (
              <button 
                onClick={handleVoiceButtonClick}
                className={`voice-btn ${isRecording ? 'recording' : ''}`}
                title={isRecording ? "Stop recording" : "Start voice input"}
              >
                {isRecording ? <Square size={16} /> : <Mic size={16} />}
              </button>
            )}
            <button 
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isTyping || isRecording}
              className="send-btn"
            >
              <Send size={16} />
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default FraudChatbot;
