import Image from "next/image";

function GridShape() {
	return (
		<>
			<div className="absolute right-0 top-0 -z-1 w-full max-w-87.5 xl:max-w-112.5">
				<Image
					alt="grid"
					src="/shape/grid-01.svg"
					width={0}
					height={0}
					loading="eager"
					className="w-135 h-63.5"
					style={{ width: "100%", height: "auto" }}
				/>
			</div>

			<div className="absolute bottom-0 left-0 -z-1 w-full max-w-87.5 rotate-180 xl:max-w-112.5">
				<Image
					alt="grid"
					src="/shape/grid-01.svg"
					width={0}
					height={0}
					loading="eager"
					className="w-135 h-63.5"
					style={{ width: "100%", height: "auto" }}
				/>
			</div>
		</>
	);
}

export default GridShape;
