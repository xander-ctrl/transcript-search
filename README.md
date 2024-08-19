# YouTube Keyword Search

Search for specific keywords or phrases within the transcripts (captions) of all videos on a YouTube channel. 

## Setup and Usage

1. **Prerequisites**

   * **Libraries:** Install the required libraries using pip:
     ```bash
     pip install google-api-python-client youtube_transcript_api concurrent.futures
     ```

2. **YouTube Data API Key**

   * Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
   * Enable the YouTube Data API v3 for your project.
   * Create an API key and restrict it to the YouTube Data API v3 for security.

3. **Configuration**

   * The first time you run the script, it will prompt you to enter your YouTube Data API key. This key will be stored in a `config.json` file in the same directory as the main script.

4. **Running the Script**

   * The script will ask you to:
     * Enter the YouTube channel URL (in the format `https://www.youtube.com/@channelname`).
     * Enter the keyword or phrase you want to search for.

5. **Output**

   * The script will search through all videos on the channel and display:
     * The video title
     * A link to the video with the timestamp where the keyword was found

## Important Notes

* **Transcript Availability:** The script relies on transcripts (captions) being available for the videos. If a video doesn't have a transcript, it will be skipped.
* **Auto-Generated Captions:** While the script can work with auto-generated captions, the accuracy might vary.
* **YouTube API Quotas:** Be mindful of the [YouTube Data API usage limits](https://developers.google.com/youtube/v3/getting-started#quota).

## Disclaimer

This script is provided as-is. Use it responsibly and ensure you comply with YouTube's terms of service.