def set_voice_channel(voice_channel_id, topic):
    topic_list = topic.split('\n')
    topic_list[2] = str(voice_channel_id)
    return '\n'.join(topic_list)


def get_voice_channel_id(topic):
    topic_list = topic.split('\n')
    return None if topic_list[2] == '-1' else int(topic_list[2])




