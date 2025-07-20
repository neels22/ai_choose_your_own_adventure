"use client"
import {useState, useEffect} from 'react';
import {useRouter} from "next/navigation";
import axios from 'axios';
import LoadingStatus from "./LoadingStatus";
import StoryGame from "./StoryGame";
import {API_BASE_URL} from "../utils/util.js";


function StoryLoader({ id }: { id: number }) {
    const router = useRouter();
    const [story, setStory] = useState<any>(null);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (id) {
            loadStory(id)
        }
    }, [id])

    const loadStory = async (storyId:number) => {
        setLoading(true)
        setError(null)

        try {
            const response = await axios.get(`${API_BASE_URL}/stories/${storyId}/complete`)
            setStory(response.data)
            setLoading(false)
        } catch (err:any) {
            if (err.response?.status === 404) {
                setError("Story is not found.")
            } else {
                setError("Failed to load story")
            }
        } finally {
            setLoading(false)
        }
    }

    const createNewStory = () => {
        router.push("/")
    }

    if (loading) {
        return <LoadingStatus theme={"story"} />
    }

    if (error) {
        return <div className="story-loader">
            <div className="error-message">
                <h2>Story Not Found</h2>
                <p>{error}</p>
                <button onClick={createNewStory}>Go to Story Generator</button>
            </div>
        </div>
    }

    if (story) {
        return <div className="story-loader">
            <StoryGame story={story} onNewStory={createNewStory} />
        </div>
    }
}

export default StoryLoader;