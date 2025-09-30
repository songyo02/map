import React, { useEffect, useRef, useState } from "react";
import Papa from "papaparse";

const Map = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [filteredCategory, setFilteredCategory] = useState("전체");
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const mapRef = useRef(null);
  const googleMap = useRef(null);
  const markers = useRef([]);
  const defaultIcon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png";
  const selectedIcon = "http://maps.google.com/mapfiles/ms/icons/blue-dot.png";

  // CSV 불러오기
  useEffect(() => {
    const fetchCsvData = async () => {
      try {
        const response = await fetch(process.env.PUBLIC_URL + "/categorized_restaurants.csv");
        if (!response.ok) throw new Error("CSV 파일 로드 실패: " + response.status);
        const csvText = await response.text();

        const results = Papa.parse(csvText, { header: true, skipEmptyLines: true });
        const formattedData = results.data.map(item => ({
          name: item.name,
          category: item.category,
          lat: parseFloat(item.lat),
          lng: parseFloat(item.lng),
        }));
        setRestaurants(formattedData);
      } catch (error) {
        console.error("🚨 CSV 불러오기 실패:", error);
      }
    };
    fetchCsvData();
  }, []);

  // 지도 + 마커
  useEffect(() => {
    if (restaurants.length === 0 || typeof window.google === "undefined") return;

    if (!googleMap.current) {
      googleMap.current = new window.google.maps.Map(mapRef.current, {
        center: { lat: 36.6424, lng: 127.4890 },
        zoom: 13,
      });
    }

    // 기존 마커 제거
    markers.current.forEach(marker => marker.setMap(null));
    markers.current = [];

    const displayRestaurants = filteredCategory === "전체"
      ? restaurants
      : restaurants.filter(r => r.category === filteredCategory);

    displayRestaurants.forEach(r => {
      if (!isNaN(r.lat) && !isNaN(r.lng)) {
        const marker = new window.google.maps.Marker({
          position: { lat: r.lat, lng: r.lng },
          map: googleMap.current,
          title: r.name,
          icon: defaultIcon,
        });

        const handleClick = () => {
          setSelectedRestaurant(r);
          googleMap.current.panTo({ lat: r.lat, lng: r.lng });

          // 이전 선택된 마커 초기화
          markers.current.forEach(m => {
            m.setIcon(defaultIcon);
            m.setAnimation(null);
          });

          // 현재 마커 강조
          marker.setIcon(selectedIcon);
          marker.setAnimation(window.google.maps.Animation.BOUNCE);
          setTimeout(() => marker.setAnimation(null), 1400);
        };

        marker.addListener("click", handleClick);
        markers.current.push(marker);
      }
    });

    if (markers.current.length > 0) {
      const bounds = new window.google.maps.LatLngBounds();
      markers.current.forEach(marker => bounds.extend(marker.getPosition()));
      googleMap.current.fitBounds(bounds);
    }
  }, [restaurants, filteredCategory]);

  const categories = ["전체", ...Array.from(new Set(restaurants.map(r => r.category)))];

  // 카드 닫기 함수
  const closeCard = () => {
    if (selectedRestaurant) {
      const marker = markers.current.find(m => m.getTitle() === selectedRestaurant.name);
      if (marker) marker.setIcon(defaultIcon); // 마커 색상 원복
      setSelectedRestaurant(null);
    }
  };

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      {/* 카테고리 필터 */}
      <div style={{ position: "absolute", zIndex: 2, padding: "10px", background: "white" }}>
        <label>
          카테고리:
          <select
            value={filteredCategory}
            onChange={e => {
              setFilteredCategory(e.target.value);
              setSelectedRestaurant(null); // 필터 변경 시 선택 해제
            }}
            style={{ marginLeft: "8px" }}
          >
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </label>
      </div>

      {/* 지도 */}
      <div
        ref={mapRef}
        style={{ width: "100%", height: "100%" }}
      />

      {/* 선택된 식당 카드 */}
      {selectedRestaurant && (
        <div
          style={{
            position: "absolute",
            top: "80px",
            right: "20px",
            zIndex: 3,
            background: "rgba(255,255,255,0.95)",
            borderRadius: "12px",
            padding: "16px",
            minWidth: "200px",
            boxShadow: "0 6px 20px rgba(0,0,0,0.3)",
            transition: "all 0.3s ease",
            cursor: "pointer",
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <h3 style={{ margin: 0, fontSize: "16px" }}>{selectedRestaurant.name}</h3>
              <p style={{ margin: "4px 0 0 0", fontSize: "14px", color: "#555" }}>
                카테고리: {selectedRestaurant.category}
              </p>
            </div>
            <button
              onClick={closeCard}
              style={{
                background: "transparent",
                border: "none",
                fontSize: "18px",
                cursor: "pointer",
                color: "#888",
                fontWeight: "bold",
              }}
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Map;
