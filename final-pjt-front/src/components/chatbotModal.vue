<template>
    <div v-if="chatbotStore.isOpen" class="chat-modal">
      <div class="chat-modal-content">
        <header>
          <h2>챗봇 상담</h2>
          <button class="close-btn" @click="chatbotStore.closeModal">X</button>
        </header>
        <div class="chat-body" ref="messagesContainer">
          <!-- 메시지 목록 -->
          <div class="messages">
            <div
              v-for="(message, index) in chatbotStore.messages"
              :key="index"
              :class="['message-container', message.role]"
            >
              <!-- 챗봇 메시지 -->
              <div
                v-if="message.role === 'assistant'"
                class="message-bubble assistant-message"
              >
                <div class="chatbot-icon">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 0 24"
                    fill="currentColor"
                    class="icon"
                  >
                    <circle cx="12" cy="12" r="10" fill="#b2d8a5" />
                    <circle cx="9" cy="10" r="1.5" fill="#6d6a5d" />
                    <circle cx="15" cy="10" r="1.5" fill="#6d6a5d" />
                    <path
                      d="M9 15h6a1 1 0 0 1 0 2H9a1 1 0 1 1 0-2z"
                      fill="#6d6a5d"
                    />
                  </svg>
                </div>
                <p>{{ message.content }}</p>
              </div>
  
              <!-- 사용자 메시지 -->
              <div
                v-else
                class="message-bubble user-message"
              >
                <p>{{ message.content }}</p>
              </div>
            </div>
          </div>
        </div>
        <!-- 입력 필드 -->
        <div class="input-container">
          <textarea
            v-model="newMessage"
            placeholder="메시지를 입력하세요..."
            @keyup.enter="handleSendMessage"
          ></textarea>
          <button @click="handleSendMessage">전송</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch, nextTick } from "vue";
  import { useChatbotStore } from "@/stores/chatbot";
  
  const chatbotStore = useChatbotStore();
  const newMessage = ref("");
  const messagesContainer = ref(null);
  
  // 메시지 전송 후 동작
  const handleSendMessage = async () => {
    if (newMessage.value.trim()) {
      chatbotStore.sendMessage(newMessage.value);
      newMessage.value = "";
      await nextTick();
      scrollToBottom();
    }
  };
  
  // 자동 스크롤 함수
  const scrollToBottom = () => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  };
  
  // 메시지 변경 감지 (새로운 메시지가 추가될 때 스크롤 아래로 이동)
  watch(
    () => chatbotStore.messages,
    async () => {
      await nextTick();
      scrollToBottom();
    },
    { deep: true }
  );
  
  // 초기화 시 마지막 메시지로 스크롤
  onMounted(() => {
    scrollToBottom();
  });
  </script>
  
  <style scoped>
  .chat-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .chat-modal-content {
    width: 400px;
    max-height: 600px;
    background: #fdf6e4; /* 연한 노랑 */
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  
  header {
    background: #d7c4a1; /* 연한 갈색 */
    color: #52493e; /* 짙은 갈색 */
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .close-btn {
    background: none;
    border: none;
    color: #52493e;
    font-size: 16px;
    cursor: pointer;
  }
  
  .chat-body {
    flex: 1;
    padding: 10px;
    background: #e9f5db; /* 연한 초록 */
    overflow-y: auto; /* 스크롤 활성화 */
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .messages {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  /* 메시지 스타일 */
  .message-container {
    display: flex;
    align-items: flex-start;
  }
  
  .message-container.user {
    justify-content: flex-end; /* 사용자 메시지는 오른쪽 */
  }
  
  .message-container.assistant {
    justify-content: flex-start; /* 챗봇 메시지는 왼쪽 */
  }
  
  .message-bubble {
    max-width: 70%;
    padding: 10px;
    border-radius: 8px;
    word-wrap: break-word;
    text-align: left;
  }
  
  .assistant-message {
    background: #d7c4a1; /* 연한 갈색 */
    color: #52493e;
    margin-right: auto;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .user-message {
    background: #ffe6a7; /* 연한 노랑 */
    color: #52493e;
    margin-left: auto;
  }
  
  /* 챗봇 아이콘 */
  .chatbot-icon {
    margin-right: 8px;
  }
  
  .chatbot-icon .icon {
    width: 30px;
    height: 30px;
  }
  
  .input-container {
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 10px;
    background: #d7c4a1; /* 연한 갈색 */
  }
  
  textarea {
    flex: 1;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 5px;
    resize: none;
    background: #fffceb; /* 밝은 노랑 */
  }
  
  button {
    background: #b2d8a5; /* 연한 초록 */
    color: #52493e;
    border: none;
    padding: 8px 12px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background: #9ecb8c; /* 약간 더 짙은 초록 */
  }
  </style>
  