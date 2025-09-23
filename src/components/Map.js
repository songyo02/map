import React, { useEffect, useRef, useState } from "react";
import Papa from "papaparse";

const Map = () => {
  const [restaurants, setRestaurants] = useState([]);
  const mapRef = useRef(null);
  const googleMap = useRef(null);
  const markers = useRef([]);

  // 1. CSV 파일 불러오기 및 파싱
  useEffect(() => {
    const fetchCsvData = async () => {
      try {
        const response = await fetch(process.env.PUBLIC_URL + "/categorized_restaurants.csv");
        if (!response.ok) throw new Error("CSV 파일 로드 실패: " + response.status);
        const csvText = await response.text();

        const results = Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
        });

        const formattedData = results.data.map(item => ({
          name: item.name,
          category: item.category,
          lat: parseFloat(item.lat),
          lng: parseFloat(item.lng),
        }));
        
        console.log("📢 PapaParse 파싱 완료:", formattedData.length, "개 항목");
        console.log("📢 첫 3개 항목:", formattedData.slice(0, 3));
        setRestaurants(formattedData);
      } catch (error) {
        console.error("🚨 CSV 불러오기 실패:", error);
      }
    };
    fetchCsvData();
  }, []);

  // 2. 지도 초기화 및 마커 표시
  useEffect(() => {
    // window.google 객체가 존재하는지 확인하여 API 로딩을 기다립니다.
    if (restaurants.length === 0 || typeof window.google === "undefined") {
      console.log("🔴 지도 생성 조건 미달 (데이터 없음 또는 Google Maps 미로드)");
      return;
    }

    if (!googleMap.current) {
      googleMap.current = new window.google.maps.Map(mapRef.current, {
        center: { lat: 36.6424, lng: 127.4890 },
        zoom: 13,
      });
      console.log("🟡 지도 초기화 완료");
    }

    // 기존 마커 제거
    markers.current.forEach(marker => marker.setMap(null));
    markers.current = [];

    // 새 마커 추가
    restaurants.forEach((r, idx) => {
      const lat = r.lat;
      const lng = r.lng;

      if (isNaN(lat) || isNaN(lng)) {
        console.log(`📍 ${idx + 1}: 유효하지 않은 좌표, 스킵`, r);
        return;
      }

      const position = { lat, lng };
      const marker = new window.google.maps.Marker({
        position,
        map: googleMap.current,
        title: r.name,
      });

      markers.current.push(marker);
    });

    console.log(`🟢 ${markers.current.length}개의 마커 생성 완료`);

    if (markers.current.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      markers.current.forEach(marker => bounds.extend(marker.getPosition()));
      googleMap.current.fitBounds(bounds);
    }
  }, [restaurants]);

  return (
    <div>
      <div
        ref={mapRef}
        style={{ width: "100%", height: "600px", marginTop: "10px" }}
      />
    </div>
  );
};

export default Map;