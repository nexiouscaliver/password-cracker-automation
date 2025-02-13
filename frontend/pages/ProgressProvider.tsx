import { ProgressProvider } from "../context/ProgressContext";
import "../styles/globals.css";

function MyApp({ Component, pageProps }) {
  return (
    <ProgressProvider>
      <Component {...pageProps} />
    </ProgressProvider>
  );
}

export default MyApp;