import streamlit as st

# ---------- Song Class ----------
class Song:
    def __init__(self, title, artist, songfile):
        self.title = title
        self.artist = artist
        self.songfile = songfile  # bytes
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"


# ---------- MusicPlaylist Class ----------
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, songfile):
        new_song = Song(title, artist, songfile)

        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song

        self.length += 1
        st.success(f"Added: {new_song}")

    def display_playlist(self):
        songs = []
        current = self.head
        i = 1
        while current:
            songs.append(f"{i}. {current}")
            current = current.next_song
            i += 1
        return songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
            st.audio(self.current_song.songfile)
        else:
            st.warning("Playlist is empty or no song selected.")

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        else:
            st.warning("End of playlist.")

    def prev_song(self):
        if self.current_song == self.head or self.head is None:
            st.warning("Already at first song.")
            return

        current = self.head
        while current.next_song != self.current_song:
            current = current.next_song
        self.current_song = current

    def delete_song(self, title):
        if self.head is None:
            st.error("Playlist is empty.")
            return

        if self.head.title == title:
            self.head = self.head.next_song
            self.current_song = self.head
            self.length -= 1
            st.success(f"Deleted: {title}")
            return

        prev = self.head
        current = self.head.next_song

        while current:
            if current.title == title:
                prev.next_song = current.next_song
                if self.current_song == current:
                    self.current_song = prev
                self.length -= 1
                st.success(f"Deleted: {title}")
                return
            prev = current
            current = current.next_song

        st.error("Song not found.")

    def get_length(self):
        return self.length


# ---------- Streamlit UI ----------
st.title("ᯓ‎𝄞 Music Playlist App")

if "playlist" not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# ---------- Sidebar: Add Song ----------
st.sidebar.header("✚ Add Song")
title = st.sidebar.text_input("Title")
artist = st.sidebar.text_input("Artist")
audio_file = st.sidebar.file_uploader(
    "Upload Audio File",
    type=["mp3", "wav", "ogg"]
)

if st.sidebar.button("Add Song to Playlist"):
    if title and artist and audio_file:
        st.session_state.playlist.add_song(
            title,
            artist,
            audio_file.read()
        )
    else:
        st.sidebar.warning("Please enter title, artist, and audio file.")

# ---------- Sidebar: Delete Song ----------
st.sidebar.markdown("---")
st.sidebar.header("🗑 Delete Song")
delete_title = st.sidebar.text_input("Song Title to Delete")

if st.sidebar.button("Delete Song"):
    st.session_state.playlist.delete_song(delete_title)

# ---------- Playlist Display ----------
st.header("Your Current Playlist")
playlist = st.session_state.playlist.display_playlist()

if playlist:
    for song in playlist:
        st.write(song)
else:
    st.write("Playlist is empty.")

# ---------- Playback Controls ----------
st.markdown("---")
st.header("Playback Controls")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⏮ Previous"):
        st.session_state.playlist.prev_song()
        st.session_state.playlist.play_current_song()

with col2:
    if st.button("▶ Play"):
        st.session_state.playlist.play_current_song()

with col3:
    if st.button("⏭ Next"):
        st.session_state.playlist.next_song()
        st.session_state.playlist.play_current_song()

st.markdown("---")
st.write(f"Total songs: {st.session_state.playlist.get_length()}")