// src/hooks/useGoogleMapsApi.js

import { useState, useEffect } from "react";

const GOOGLE_MAPS_API_KEY = "AIzaSyBCyU2qprBvlv8MriekBO86iTzNb8IIpuE"; // 여기에 API 키 입력

const useGoogleMapsApi = () => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    // API가 이미 로드되었는지 확인
    if (window.google) {
      setIsLoaded(true);
      return;
    }

    // 스크립트가 이미 DOM에 추가되었는지 확인
    if (document.querySelector(`script[src*="googlemaps.com"]`)) {
      return;
    }

    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}`;
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);

    script.onload = () => {
      setIsLoaded(true);
      console.log("✅ Google Maps API 로드 완료");
    };

    script.onerror = () => {
      console.error("🚨 Google Maps API 로드 실패");
    };
  }, []);

  return isLoaded;
};

export default useGoogleMapsApi;