import streamlit as st
from confluent_kafka import Producer
import json

# Kafka Configuration
conf = {
    'bootstrap.servers': "pkc-921jm.us-east-2.aws.confluent.cloud:9092",
    'security.protocol': "SASL_SSL",
    'sasl.mechanisms': "PLAIN",
    'sasl.username': '6KE3HKBM46CFQYGL',
    'sasl.password': 'uD/s8CeKResFVUYM1Psj3E0QbdHq+BI5mn03VkLMicY8jBm/o/sd1JA8D74xGskn'
}

KAFKA_TOPIC = 'trendpulse'

# Initialize Kafka Producer
try:
    producer = Producer(conf)
    st.success("✅ Kafka Producer Initialized Successfully")
except Exception as e:
    st.error(f"❌ Kafka Producer Initialization Failed: {e}")

# Streamlit UI
st.title("📢 Post or Comment")

# User Input: Name
name = st.text_input("Enter your name:")

# User Selection: Post or Comment
option = st.radio("What would you like to do?", ("Post", "Comment"))

# Text area for writing
message = st.text_area(f"Write your {option.lower()} here:")

# Send Button
if st.button("Send"):
    if not name:
        st.warning("⚠️ Please enter your name before sending.")
    elif not message.strip():
        st.warning(f"⚠️ Your {option.lower()} cannot be empty.")
    else:
        # Prepare data
        data = {
            "name": name,
            "type": option,
            "message": message
        }
        try:
            # Send data to Kafka
            producer.produce(KAFKA_TOPIC, key=name, value=json.dumps(data))
            producer.flush()
            st.success(f"✅ {name}, your {option.lower()} has been sent to Kafka successfully!")
            st.write(f"**{option} by {name}:** {message}")
        except Exception as e:
            st.error(f"❌ Failed to send data to Kafka: {e}")
