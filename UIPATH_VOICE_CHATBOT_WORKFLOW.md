# 🎤 **UiPath Studio 2025 - Voice-Enabled Smart Chatbot Workflow**

## **📋 Overview**

This guide provides step-by-step instructions to update your UiPath workflow to test the new **voice-enabled chatbot** with **improved NLP** (Natural Language Processing).

---

## **🆕 What's New in the Chatbot**

### **1. Voice Recording (WhatsApp-Style)**
- **Mic button** next to send button
- Click to start recording (turns red)
- Speak your message
- Click stop (square icon) to finish
- Text appears in input field automatically
- Then click send

### **2. Improved NLP**
The chatbot now understands:
- **Greetings**: "hi", "hello", "hey", "good morning"
- **Gratitude**: "thank you", "thanks", "appreciate it"
- **Farewells**: "bye", "goodbye", "see you later"
- **Help requests**: "help", "what can you do", "commands"
- **Transaction analysis**: "analyze $500 from Starbucks", "check transaction"
- **System status**: "how's the system", "is it working", "health check"
- **Statistics**: "show stats", "fraud rate", "metrics"
- **Compliments**: "good job", "excellent", "amazing"

**Example variations it understands:**
- "Check system health" = "How's the system?" = "Is everything working?"
- "Analyze a transaction" = "Check this transaction" = "Is this fraud?"

---

## **🔧 Updated UiPath Workflow**

### **Step 1: Update Variables**

Open your `Main.xaml` and update the Variables panel:

| Variable Name | Type | Scope | Default Value |
|---------------|------|-------|---------------|
| `Commands` | String[] | Sequence | `{"Check system health", "How's the system doing", "Analyze $500 from Amazon", "Show me fraud statistics", "Thanks for your help"}` |
| `ResponseText` | String | Sequence | (empty) |
| `VoiceTestEnabled` | Boolean | Sequence | `True` |
| `TestVoiceCommands` | String[] | Sequence | `{"voice_test_1", "voice_test_2"}` |

---

### **Step 2: Main Workflow Structure**

Replace your current workflow with this enhanced version:

```
Main.xaml
├── Sequence: "Enhanced Chatbot Testing"
│   ├── Use Application/Browser: "Edge Fraud Detection System"
│   │   ├── Sequence: "Test NLP Variations"
│   │   │   ├── For Each: Commands
│   │   │   │   ├── Type Into: Chatbot Input
│   │   │   │   ├── Delay: 2 seconds
│   │   │   │   ├── Click: Send Button
│   │   │   │   ├── Delay: 3 seconds
│   │   │   │   ├── Get Text: Bot Response
│   │   │   │   ├── Log Message: Command + Response
│   │   │   │   └── Take Screenshot
│   │   │   └── End For Each
│   │   ├── Sequence: "Test Voice Recording"
│   │   │   ├── Click: Voice/Mic Button
│   │   │   ├── Delay: 1 second (mic activates)
│   │   │   ├── Get Text: Input Field (should show transcribed text)
│   │   │   ├── Click: Stop Recording (Square button)
│   │   │   ├── Delay: 2 seconds
│   │   │   ├── Click: Send Button
│   │   │   ├── Get Text: Bot Response
│   │   │   ├── Log Message: Voice test result
│   │   │   └── Take Screenshot
│   │   └── End Sequence
│   └── End Use Application
└── End Sequence
```

---

## **📝 Detailed Activity Configuration**

### **Activity 1: Use Application/Browser (Edge)**

**What to do:**
1. Drag **"Use Application/Browser"** from Activities panel
2. Click **"Indicate application to automate"**
3. Open Edge browser with `http://localhost:3000/dashboard`
4. Click on the browser window when UiPath highlights it

**Properties:**
- **Input Mode**: `Hardware Events`
- **Open**: `Never`
- **Browser Type**: `Edge`

---

### **Activity 2: For Each Loop - Test NLP Commands**

**What to do:**
1. Drag **"For Each"** activity inside Use Application
2. Set **TypeArgument**: `String`
3. Set **Values**: `Commands` (your variable)
4. Name the item: `currentCommand`

**Inside the loop, add these activities:**

#### **2a. Type Into - Chatbot Input**

**What to do:**
1. Drag **"Type Into"** activity
2. Click **"Indicate element"**
3. **Open chatbot** by clicking the blue circular button (bottom-right)
4. Click on the **input field** (where it says "Type or speak your message...")

**Properties:**
- **Text**: `currentCommand`
- **Delay between keys**: `50` milliseconds
- **Empty field**: `Yes` (clears field before typing)
- **Click before typing**: `Yes`

**Selector** (auto-generated, should look like):
```xml
<webctrl tag='INPUT' class='message-input' />
```

---

#### **2b. Delay**

**What to do:**
1. Drag **"Delay"** activity
2. Set **Duration**: `00:00:02` (2 seconds)

**Why**: Gives chatbot time to process

---

#### **2c. Click - Send Button**

**What to do:**
1. Drag **"Click"** activity
2. Click **"Indicate element"**
3. Click on the **Send button** (paper plane icon)

**Properties:**
- **Click Type**: `Single`
- **Mouse Button**: `Left`

**Selector**:
```xml
<webctrl tag='BUTTON' class='send-btn' />
```

---

#### **2d. Delay (Wait for Response)**

**What to do:**
1. Drag **"Delay"** activity
2. Set **Duration**: `00:00:03` (3 seconds)

**Why**: Waits for bot to respond

---

#### **2e. Get Text - Bot Response**

**What to do:**
1. Drag **"Get Text"** activity
2. Click **"Indicate element"**
3. Click on the **chatbot messages area** (where bot responses appear)

**Properties:**
- **Output**: `ResponseText` (your variable)

**Selector**:
```xml
<webctrl tag='DIV' class='chatbot-messages' />
```

---

#### **2f. Log Message**

**What to do:**
1. Drag **"Log Message"** activity
2. Set **Message**: `"Command: " + currentCommand + " | Response: " + ResponseText`
3. Set **Level**: `Info`

---

#### **2g. Take Screenshot**

**What to do:**
1. Drag **"Take Screenshot"** activity
2. Click **"Indicate element"**
3. Select the entire **chatbot window**

**Properties:**
- **Save to**: `"Screenshots\nlp_test_" + currentCommand.Replace(" ", "_") + ".png"`

---

### **Activity 3: Test Voice Recording**

**Add this sequence AFTER the For Each loop:**

#### **3a. Click - Voice/Mic Button**

**What to do:**
1. Drag **"Click"** activity
2. Click **"Indicate element"**
3. Click on the **green microphone button** (circular, next to send button)

**Properties:**
- **Click Type**: `Single`

**Selector**:
```xml
<webctrl tag='BUTTON' class='voice-btn' />
```

**Visual Cue**: Button turns RED when recording starts

---

#### **3b. Delay (Recording Time)**

**What to do:**
1. Drag **"Delay"** activity
2. Set **Duration**: `00:00:01` (1 second)

**Why**: Simulates speaking time

**Note**: In real testing, you would speak during this time. For automation, we'll just verify the button state changes.

---

#### **3c. Get Text - Check Input Field**

**What to do:**
1. Drag **"Get Text"** activity
2. Target the **input field**
3. Store in variable: `ResponseText`

**Why**: Verifies that voice transcription populated the field

---

#### **3d. Click - Stop Recording**

**What to do:**
1. Drag **"Click"** activity
2. Click **"Indicate element"**
3. Click on the **red square button** (stop recording)

**Selector**:
```xml
<webctrl tag='BUTTON' class='voice-btn recording' />
```

---

#### **3e. Verify Recording Indicator**

**What to do:**
1. Drag **"Element Exists"** activity
2. Target the **recording indicator** (red bar with timer at top)
3. Store result in: `recordingIndicatorExists` (Boolean variable)

**Selector**:
```xml
<webctrl tag='DIV' class='recording-indicator' />
```

---

#### **3f. Log Voice Test Result**

**What to do:**
1. Drag **"Log Message"** activity
2. Set **Message**: `"Voice test completed. Recording indicator found: " + recordingIndicatorExists.ToString()`

---

#### **3g. Take Screenshot - Voice Test**

**What to do:**
1. Drag **"Take Screenshot"** activity
2. Save to: `"Screenshots\voice_test_result.png"`

---

## **🎯 Complete XAML Structure**

Here's the updated Main.xaml structure you should build:

```xml
<Sequence DisplayName="Enhanced Chatbot Testing">
  <Sequence.Variables>
    <Variable Name="Commands" Type="String[]" Default="{&quot;Check system health&quot;, &quot;How's the system doing&quot;, &quot;Analyze $500 from Amazon&quot;, &quot;Show me fraud statistics&quot;, &quot;Thanks for your help&quot;}" />
    <Variable Name="ResponseText" Type="String" />
    <Variable Name="VoiceTestEnabled" Type="Boolean" Default="True" />
    <Variable Name="recordingIndicatorExists" Type="Boolean" />
  </Sequence.Variables>
  
  <!-- Use Application/Browser -->
  <uix:NApplicationCard DisplayName="Edge Fraud Detection System">
    <uix:NApplicationCard.Body>
      <ActivityAction>
        <Sequence DisplayName="Test Chatbot Features">
          
          <!-- Open Chatbot -->
          <uix:NClick DisplayName="Click Chatbot Trigger">
            <!-- Selector: <webctrl tag='DIV' class='chatbot-trigger' /> -->
          </uix:NClick>
          
          <Delay Duration="00:00:02" />
          
          <!-- Test NLP Commands -->
          <ForEach TypeArgument="String" Values="[Commands]" DisplayName="For Each NLP Command">
            <ActivityAction Argument="currentCommand">
              <Sequence DisplayName="Test Command">
                
                <!-- Type command -->
                <uix:NTypeInto Text="[currentCommand]" DisplayName="Type Into Chatbot">
                  <!-- Selector: <webctrl tag='INPUT' class='message-input' /> -->
                </uix:NTypeInto>
                
                <Delay Duration="00:00:02" />
                
                <!-- Click Send -->
                <uix:NClick DisplayName="Click Send Button">
                  <!-- Selector: <webctrl tag='BUTTON' class='send-btn' /> -->
                </uix:NClick>
                
                <Delay Duration="00:00:03" />
                
                <!-- Get Response -->
                <uix:NGetText TextString="[ResponseText]" DisplayName="Get Bot Response">
                  <!-- Selector: <webctrl tag='DIV' class='chatbot-messages' /> -->
                </uix:NGetText>
                
                <!-- Log Result -->
                <LogMessage Message="[&quot;Command: &quot; + currentCommand + &quot; | Response: &quot; + ResponseText]" Level="Info" />
                
                <!-- Screenshot -->
                <TakeScreenshot FileName="[&quot;Screenshots\nlp_test_&quot; + currentCommand.Replace(&quot; &quot;, &quot;_&quot;) + &quot;.png&quot;]" />
                
              </Sequence>
            </ActivityAction>
          </ForEach>
          
          <!-- Test Voice Recording -->
          <If Condition="[VoiceTestEnabled]">
            <If.Then>
              <Sequence DisplayName="Voice Recording Test">
                
                <!-- Click Mic Button -->
                <uix:NClick DisplayName="Click Voice Button">
                  <!-- Selector: <webctrl tag='BUTTON' class='voice-btn' /> -->
                </uix:NClick>
                
                <Delay Duration="00:00:01" />
                
                <!-- Check if recording indicator appears -->
                <uix:NElementExists Exists="[recordingIndicatorExists]" DisplayName="Check Recording Indicator">
                  <!-- Selector: <webctrl tag='DIV' class='recording-indicator' /> -->
                </uix:NElementExists>
                
                <!-- Click Stop (Square button) -->
                <uix:NClick DisplayName="Click Stop Recording">
                  <!-- Selector: <webctrl tag='BUTTON' class='voice-btn recording' /> -->
                </uix:NClick>
                
                <Delay Duration="00:00:02" />
                
                <!-- Log Result -->
                <LogMessage Message="[&quot;Voice test completed. Recording indicator: &quot; + recordingIndicatorExists.ToString()]" Level="Info" />
                
                <!-- Screenshot -->
                <TakeScreenshot FileName="Screenshots\voice_test_result.png" />
                
              </Sequence>
            </If.Then>
          </If>
          
        </Sequence>
      </ActivityAction>
    </uix:NApplicationCard.Body>
  </uix:NApplicationCard>
  
</Sequence>
```

---

## **🎨 Visual Guide - What to Click**

### **1. Chatbot Trigger Button**
- **Location**: Bottom-right corner of screen
- **Appearance**: Blue circular button with message icon
- **Pulsing animation**: Yes

### **2. Chatbot Input Field**
- **Location**: Bottom of chatbot window
- **Placeholder**: "Type or speak your message..."
- **Appearance**: White/gray rounded input box

### **3. Voice/Mic Button**
- **Location**: Between input field and send button
- **Appearance**: 
  - **Idle**: Green circular button with microphone icon
  - **Recording**: Red circular button with square (stop) icon
  - **Animation**: Pulsing red glow when recording

### **4. Send Button**
- **Location**: Right side of input field
- **Appearance**: Blue button with paper plane icon

### **5. Recording Indicator**
- **Location**: Above input field (appears when recording)
- **Appearance**: Red bar with timer (e.g., "0:05")
- **Icon**: Sound wave icon (blinking)

---

## **📊 Expected Results**

### **NLP Test Results**

| Command | Expected Bot Response |
|---------|----------------------|
| "Check system health" | "✅ System Status: All models loaded and operational..." |
| "How's the system doing" | Same as above (NLP understands variation) |
| "Analyze $500 from Amazon" | "🔍 Analyzing transaction... Risk Score: X%..." |
| "Show me fraud statistics" | "📊 Current Statistics: Total Transactions: X..." |
| "Thanks for your help" | "You're welcome! Happy to help..." |

### **Voice Test Results**

1. **Mic button clicked**: Turns red, starts pulsing
2. **Recording indicator**: Red bar appears with timer
3. **Stop clicked**: Recording stops, button returns to green
4. **Input field**: Should contain transcribed text (if voice was used)

---

## **🐛 Troubleshooting**

### **Issue 1: Voice button not found**
**Solution**: 
- Voice feature requires Chrome or Edge browser
- Check if `isVoiceSupported` is true in browser console
- Try refreshing the page

### **Issue 2: Selectors not working**
**Solution**:
- Use **UiPath's "Indicate element"** feature
- Enable **"Use Fuzzy Selector"** in properties
- Try **"Anchor Base"** activity if element is hard to find

### **Issue 3: Bot not responding**
**Solution**:
- Increase delay times (3-5 seconds)
- Check if Flask backend is running (`python flask_server.py`)
- Verify chatbot is open before typing

### **Issue 4: Recording indicator not appearing**
**Solution**:
- Browser must support Web Speech API
- Check browser permissions for microphone
- Test manually first before automation

---

## **✅ Testing Checklist**

- [ ] Chatbot opens when trigger clicked
- [ ] All NLP command variations work
- [ ] Bot understands different phrasings
- [ ] Voice button appears (green mic icon)
- [ ] Voice button turns red when clicked
- [ ] Recording indicator shows timer
- [ ] Stop button (square) appears when recording
- [ ] Input field updates with voice text
- [ ] Send button works after voice input
- [ ] Screenshots saved correctly
- [ ] Log messages show all test results

---

## **🚀 Advanced Features to Test**

### **Wake Word Activation** (Future Enhancement)
```
1. Say "Hey Fraud Detector"
2. Chatbot activates automatically
3. Speak your command
4. Bot processes and responds
```

### **Context-Aware Conversations**
```
User: "Show high-risk transactions"
Bot: "Here are 5 high-risk transactions..."
User: "What about yesterday?" ← Bot remembers context
Bot: "Yesterday's high-risk transactions: ..."
```

---

## **📁 File Structure After Testing**

```
UiPath_Studio_Project/
├── Main.xaml (updated workflow)
├── project.json
├── Screenshots/
│   ├── nlp_test_Check_system_health.png
│   ├── nlp_test_Hows_the_system_doing.png
│   ├── nlp_test_Analyze_$500_from_Amazon.png
│   ├── nlp_test_Show_me_fraud_statistics.png
│   ├── nlp_test_Thanks_for_your_help.png
│   └── voice_test_result.png
└── Logs/
    └── execution_log.txt
```

---

## **🎓 Summary**

### **What You Built:**
1. ✅ NLP testing for multiple command variations
2. ✅ Voice recording button testing
3. ✅ Recording indicator verification
4. ✅ Automated screenshot capture
5. ✅ Comprehensive logging

### **What the Chatbot Can Do:**
1. ✅ Understand natural language variations
2. ✅ Accept voice input (WhatsApp-style)
3. ✅ Show recording timer
4. ✅ Transcribe speech to text
5. ✅ Process and respond intelligently

### **Next Steps:**
1. Run the workflow in UiPath Studio
2. Review screenshots in `Screenshots/` folder
3. Check logs for test results
4. Test voice feature manually
5. Expand NLP commands as needed

---

**Your chatbot is now voice-enabled with smart NLP! 🎤🤖**
