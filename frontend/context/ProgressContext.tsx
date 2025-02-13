import { createContext, useContext, useState, ReactNode} from "react";

interface ProgressContextType {
    progress: number;
    setProgress: (progress: number) => void;
}

const ProgressContext = createContext<ProgressContextType | undefined>(undefined);

export const ProgressProvider = ( {children}: { children: ReactNode }) => {
    const [progress, setProgress] = useState(0);

    return (
        <ProgressContext.Provider value={{ progress, setProgress }}>
            {children}
        </ProgressContext.Provider>
    );
};


export const useProgress = () => {
    const context = useContext(ProgressContext);
    if (context === undefined) {
        throw new Error("useProgress must be used within a ProgressProvider");
    }
    return context;
};