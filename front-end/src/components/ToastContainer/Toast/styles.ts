import styled, { css } from "styled-components";
import { animated } from "react-spring";

const ToastTypeVariations = {
  info: css`
    background: #ebf8ff;
    color: #3172b7;
  `,
  success: css`
    background: #e6fffa;
    color: #2e656a;
  `,
  error: css`
    background: #fddede;
    color: #c53030;
  `,
  music: css`
    background: #353535;
    color: #f5f5f5;
  `
};

interface ContainerProps {
  type?: 'success' | 'error' | 'info' | 'music';
  hasDescription: number;
}
export const Container = styled(animated.div)<ContainerProps>`
  width: 320px;
  position: relative;
  padding: 5px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
  display: flex;

  & + div {
    margin-top: 8px;
  }

  ${(props) => ToastTypeVariations[props.type || "info"]}
  > svg {
    margin: 4px 12px 0 0;
  }

  ${(props) => ToastTypeVariations[props.type || "music"]}
  > img {
    width: auto;
    height: 4rem;
    margin-right: 0.5rem;
  }

  div {
    flex: 1;
    p {
      margin-top: 4px;
      font-size: 14px;
      opacity: 0.8;
      line-height: 20px;
    }
  }
  button {
    position: absolute;
    right: 4px;
    top: 4px;
    border: 0;
    background: transparent;
    color: inherit;
  }

  ${(props) =>
    !props.hasDescription &&
    css`
      align-items: center;
      svg {
        margin-top: 0;
      }
    `}
`;
