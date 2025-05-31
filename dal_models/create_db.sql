-- 1. Таблица Users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    tg_id INT NOT NULL
);

-- 2. Таблица BotStorages
CREATE TABLE botstorages (
    bot_id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Таблица Channels
CREATE TABLE channels (
    channel_id SERIAL PRIMARY KEY,
    channel_username INT NOT NULL,
    channel_title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bot_id INT REFERENCES botstorages(bot_id)
);

-- 4. Таблица Styles
CREATE TABLE styles (
    style_id SERIAL PRIMARY KEY,
    parameters TEXT
);
-- 5. Таблица Tags
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name TEXT NOT NULL
);

-- 6. Таблица Sources
CREATE TABLE sources (
    source_id SERIAL PRIMARY KEY,
    source_name TEXT NOT NULL
);

-- 7. Таблица SourceTag (связь многие ко многим)
CREATE TABLE sourcetag (
    source_id INT REFERENCES sources(source_id),
    tag_id INT REFERENCES tags(tag_id),
    PRIMARY KEY (source_id, tag_id)
);

-- 8. Таблица Prompts
CREATE TABLE prompts (
    prompt_id SERIAL PRIMARY KEY,
    prompt_text TEXT NOT NULL,
    style_id INT REFERENCES styles(style_id),
    user_id INT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Таблица Images
CREATE TABLE images (
    image_id SERIAL PRIMARY KEY,
    image_url TEXT NOT NULL
);

-- 10. Таблица Schedules
CREATE TABLE schedules (
    schedule_id SERIAL PRIMARY KEY,
    channel_id INT REFERENCES channels(channel_id),
    publish_time TIMESTAMP,
    is_published BOOLEAN DEFAULT FALSE
);

-- 11. Таблица Posts
CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    source_id INT REFERENCES sources(source_id),
    prompt_id INT REFERENCES prompts(prompt_id),
    image_id INT REFERENCES images(image_id),
    channel_id INT REFERENCES channels(channel_id),
    schedule_id INT REFERENCES schedules(schedule_id),
    user_id INT REFERENCES users(user_id),
    content_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_at TIMESTAMP,
    scheduled_time TIMESTAMP
);