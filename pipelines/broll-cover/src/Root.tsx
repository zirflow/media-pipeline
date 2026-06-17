import React from "react";
import { Composition } from "remotion";

// ── B-roll: Animated background transition ──

const BrollScene: React.FC = () => {
  return (
    <div
      style={{
        flex: 1,
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 48,
        fontWeight: "bold",
        color: "white",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <div>Media Pipeline</div>
        <div style={{ fontSize: 24, marginTop: 16, opacity: 0.8 }}>
          Content-as-Code
        </div>
      </div>
    </div>
  );
};

// ── YouTube Thumbnail (16:9) ──

const YouTubeCover: React.FC = () => {
  return (
    <div
      style={{
        width: 1280,
        height: 720,
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 64,
        fontWeight: "bold",
        color: "white",
        fontFamily: "Arial, sans-serif",
        padding: 40,
      }}
    >
      <div style={{ textAlign: "center" }}>VIDEO TITLE</div>
      <div
        style={{
          fontSize: 32,
          marginTop: 20,
          opacity: 0.8,
          textAlign: "center",
        }}
      >
        Subtitle text
      </div>
    </div>
  );
};

// ── Xiaohongshu / Douyin Cover (9:16) ──

const VerticalCover: React.FC = () => {
  return (
    <div
      style={{
        width: 1080,
        height: 1920,
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        fontSize: 72,
        fontWeight: "bold",
        color: "white",
        fontFamily: "Arial, sans-serif",
        padding: 60,
      }}
    >
      <div style={{ textAlign: "center" }}>封面标题</div>
      <div
        style={{
          fontSize: 36,
          marginTop: 40,
          opacity: 0.8,
          textAlign: "center",
        }}
      >
        副标题文字
      </div>
    </div>
  );
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="broll"
        component={BrollScene}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
      />
      <Composition
        id="youtube-cover"
        component={YouTubeCover}
        durationInFrames={1}
        fps={30}
        width={1280}
        height={720}
      />
      <Composition
        id="xhs-cover"
        component={VerticalCover}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1920}
      />
    </>
  );
};
